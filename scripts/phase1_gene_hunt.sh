#!/bin/bash
# Phase 1.1 + 1.2 — index genomes and hunt the capsaicin-pathway genes across
# C. annuum (bell/RefSeq), C. chinense (habanero), C. baccatum (PBC81).
# Strategy: use the well-annotated C. annuum RefSeq proteome to (a) census the
# pathway genes and (b) define curated query sequences, then DIAMOND-search those
# queries against the chinense & baccatum proteomes to find orthologs by homology.
set -euo pipefail
source ~/miniforge3/etc/profile.d/conda.sh
unset PYTHONPATH
conda activate pepper

ROOT="$HOME/Desktop/Capsaicin Design Platform"
DATA="$ROOT/01-data/genomes/capsicum_refs/ncbi_dataset/data"
RES="$ROOT/03-results"
mkdir -p "$RES"

ACCS="GCF_002878395.1 GCA_002271895.2 GCA_002271885.2"
label() { case "$1" in
  GCF_002878395.1) echo "C.annuum";;
  GCA_002271895.2) echo "C.chinense";;
  GCA_002271885.2) echo "C.baccatum";;
esac; }
ANNUUM="$DATA/GCF_002878395.1/protein.faa"   # the annotated reference proteome

echo "==================================================================="
echo " PHASE 1.1  —  genome + proteome stats"
echo "==================================================================="
printf "species\tfile\tnum_seqs\tsum_len\tmin\tavg\tmax\n" > "$RES/stats.tsv"
for acc in $ACCS; do
  sp=$(label "$acc")
  gen=$(ls "$DATA/$acc/"*_genomic.fna 2>/dev/null | head -1)
  prot="$DATA/$acc/protein.faa"
  [ -f "$gen" ] && samtools faidx "$gen"
  # genome
  seqkit stats -T "$gen"  | tail -n +2 | awk -v s="$sp" 'BEGIN{FS=OFS="\t"}{print s"-genome",$1,$4,$5,$6,$7,$8}' >> "$RES/stats.tsv"
  # proteome
  seqkit stats -T "$prot" | tail -n +2 | awk -v s="$sp" 'BEGIN{FS=OFS="\t"}{print s"-proteome",$1,$4,$5,$6,$7,$8}' >> "$RES/stats.tsv"
  echo "  [$sp] genome indexed + stats done"
done
echo "-> $RES/stats.tsv"
column -t -s$'\t' "$RES/stats.tsv" | sed 's#'"$DATA"'/##g'

echo
echo "==================================================================="
echo " PHASE 1.2a  —  pathway-gene annotation census (per species)"
echo "==================================================================="
# label=regex (case-insensitive, matched against FASTA header lines)
PATS=(
"PAL=phenylalanine ammonia-lyase"
"C4H=cinnamate 4-monooxygenase|cinnamate 4-hydroxylase"
"4CL=4-coumarate.*CoA ligase"
"HCT=hydroxycinnamoyltransferase"
"COMT_CCoAOMT=caffeoyl-CoA O-methyltransferase|caffeic acid.*O-methyltransferase"
"BCAT=branched-chain.*aminotransferase"
"aminotransferase_all=aminotransferase"
"KAS=3-oxoacyl-.acyl-carrier|beta-ketoacyl"
"FAT_thioesterase=acyl-carrier-protein..*thioesterase|fatty acyl.*thioesterase"
"AT3_Pun1_CS=capsaicin synthase|acyltransferase 3"
"acyltransferase_all=acyltransferase"
"MYB_regulators=MYB"
"WRKY_regulators=WRKY"
"peroxidase_degradation=peroxidase"
)
# header: gene + 3 species
printf "gene\tC.annuum\tC.chinense\tC.baccatum\n" > "$RES/pathway_census.tsv"
for p in "${PATS[@]}"; do
  name="${p%%=*}"; rgx="${p#*=}"
  row="$name"
  for acc in $ACCS; do
    c=$(grep '^>' "$DATA/$acc/protein.faa" | grep -iEc "$rgx" || true)
    row="$row	$c"
  done
  printf "%s\n" "$row" >> "$RES/pathway_census.tsv"
done
echo "-> $RES/pathway_census.tsv"
column -t -s$'\t' "$RES/pathway_census.tsv"

echo
echo "==================================================================="
echo " PHASE 1.2b  —  build curated query set from annotated C. annuum"
echo "==================================================================="
# Specific biosynthetic enzymes only (exclude broad MYB/WRKY/peroxidase families)
UNION='phenylalanine ammonia-lyase|cinnamate 4-monooxygenase|cinnamate 4-hydroxylase|4-coumarate.*CoA ligase|hydroxycinnamoyltransferase|caffeoyl-CoA O-methyltransferase|caffeic acid.*O-methyltransferase|branched-chain.*aminotransferase|3-oxoacyl-.acyl-carrier|beta-ketoacyl|acyl-carrier-protein..*thioesterase|capsaicin synthase|acyltransferase 3'
grep '^>' "$ANNUUM" | grep -iE "$UNION" | sed 's/^>//' > "$RES/query_annotations.txt"
sed 's/ .*//' "$RES/query_annotations.txt" > "$RES/query_ids.txt"
seqkit grep -f "$RES/query_ids.txt" "$ANNUUM" > "$RES/pathway_queries.faa"
nq=$(grep -c '^>' "$RES/pathway_queries.faa" || echo 0)
echo "curated pathway queries extracted from C. annuum RefSeq: $nq proteins"
echo "-> $RES/pathway_queries.faa  (+ query_annotations.txt)"

echo
echo "==================================================================="
echo " PHASE 1.2c  —  DIAMOND ortholog search into chinense & baccatum"
echo "==================================================================="
for acc in GCA_002271895.2 GCA_002271885.2; do
  sp=$(label "$acc")
  diamond makedb --in "$DATA/$acc/protein.faa" -d "$RES/${sp}_db" --quiet
  diamond blastp -q "$RES/pathway_queries.faa" -d "$RES/${sp}_db" \
    --outfmt 6 qseqid sseqid pident length qcovhsp scovhsp evalue bitscore \
    -k 2 --evalue 1e-20 --quiet > "$RES/hits_${sp}.tsv"
  nh=$(cut -f1 "$RES/hits_${sp}.tsv" | sort -u | wc -l | tr -d ' ')
  echo "  [$sp] queries with an ortholog hit (e<1e-20): $nh / $nq  -> $RES/hits_${sp}.tsv"
done

echo
echo "==================================================================="
echo " DONE — key outputs in 03-results/:"
echo "   stats.tsv  pathway_census.tsv  pathway_queries.faa  hits_C.chinense.tsv  hits_C.baccatum.tsv"
echo "==================================================================="