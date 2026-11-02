# Scoville Splice Capsaicinoid Design Platform

**Priyanca Iyengar Ford** · [scovillesplice.farm](https://scovillesplice.farm) · ORCID [0000-0003-0395-1752](https://orcid.org/0000-0003-0395-1752)

> A 21-paper computational biology dataset spanning gene hunting, protein structure prediction, molecular docking, metabolic flux analysis, and cultivar engineering for *Capsicum* species — pushing the Scoville ceiling from ~2.2M SHU (natural Carolina Reaper) to **13.1M SHU** through rational design.

---

## Papers & Releases

Each paper has its own GitHub Release with the full PDF and HTML as downloadable assets.

| # | Title | Release | DOI |
|---|-------|---------|-----|
| 01 | Computational Design of Ten Engineered *Capsicum* Cultivars Spanning 3–13M SHU | [paper-01](../../releases/tag/paper-01) | [10.6084/m9.figshare.28170504](https://doi.org/10.6084/m9.figshare.28170504) |
| 02 | Beyond Peppers: Cross-Species Capsaicinoid Engineering | [paper-02](../../releases/tag/paper-02) | [10.6084/m9.figshare.28170507](https://doi.org/10.6084/m9.figshare.28170507) |
| 03 | Sweet Heat: Engineering Dual Capsaicinoid-Sweetener Pepper Lines | [paper-03](../../releases/tag/paper-03) | [10.6084/m9.figshare.28170510](https://doi.org/10.6084/m9.figshare.28170510) |
| 04 | The Iyengar Flavor Index: A Unified Scoring Framework | [paper-04](../../releases/tag/paper-04) | [10.6084/m9.figshare.28170513](https://doi.org/10.6084/m9.figshare.28170513) |
| 05 | Umami Engineering: GABA and Glutamate Pathway Optimization | [paper-05](../../releases/tag/paper-05) | [10.6084/m9.figshare.28170516](https://doi.org/10.6084/m9.figshare.28170516) |
| 06 | Bitter Reduction in Brassica via CYP450 Knockout | [paper-06](../../releases/tag/paper-06) | [10.6084/m9.figshare.28170519](https://doi.org/10.6084/m9.figshare.28170519) |
| 07 | Kokumi Engineering: γ-Glutamyl Peptide Accumulation | [paper-07](../../releases/tag/paper-07) | [10.6084/m9.figshare.28170522](https://doi.org/10.6084/m9.figshare.28170522) |
| 08 | Astringency Attenuation Through Proanthocyanidin Pathway Editing | [paper-08](../../releases/tag/paper-08) | [10.6084/m9.figshare.28170525](https://doi.org/10.6084/m9.figshare.28170525) |
| 09 | Cooling Compound Biosynthesis: Menthol and WS-23 Pathways | [paper-09](../../releases/tag/paper-09) | [10.6084/m9.figshare.28170528](https://doi.org/10.6084/m9.figshare.28170528) |
| 10 | TRPA1 Activation Engineering and Cross-Species Irritant Profiling | [paper-10](../../releases/tag/paper-10) | [10.6084/m9.figshare.28170531](https://doi.org/10.6084/m9.figshare.28170531) |
| 11 | The Capsaicin Design Platform: An Integrated Framework | [paper-11](../../releases/tag/paper-11) | [10.6084/m9.figshare.28170534](https://doi.org/10.6084/m9.figshare.28170534) |

### Cultivar Specifications (SS-0087 – SS-0096)

| SKU | Name | Target SHU | Release | DOI |
|-----|------|-----------|---------|-----|
| SS-0087 | Verbal Warning | 3,000,000 | [cultivar-ss-0087](../../releases/tag/cultivar-ss-0087) | [10.6084/m9.figshare.28170537](https://doi.org/10.6084/m9.figshare.28170537) |
| SS-0088 | Kill Switch | 3,600,000 | [cultivar-ss-0088](../../releases/tag/cultivar-ss-0088) | [10.6084/m9.figshare.28170540](https://doi.org/10.6084/m9.figshare.28170540) |
| SS-0089 | Hostile Agent | 4,500,000 | [cultivar-ss-0089](../../releases/tag/cultivar-ss-0089) | [10.6084/m9.figshare.28170543](https://doi.org/10.6084/m9.figshare.28170543) |
| SS-0090 | Containment Breach | 5,800,000 | [cultivar-ss-0090](../../releases/tag/cultivar-ss-0090) | [10.6084/m9.figshare.28170546](https://doi.org/10.6084/m9.figshare.28170546) |
| SS-0091 | System Shock | 7,200,000 | [cultivar-ss-0091](../../releases/tag/cultivar-ss-0091) | [10.6084/m9.figshare.28170549](https://doi.org/10.6084/m9.figshare.28170549) |
| SS-0092 | Venom Protocol | 8,500,000 | [cultivar-ss-0092](../../releases/tag/cultivar-ss-0092) | [10.6084/m9.figshare.28170552](https://doi.org/10.6084/m9.figshare.28170552) |
| SS-0093 | Level 4 Pathogen | 9,800,000 | [cultivar-ss-0093](../../releases/tag/cultivar-ss-0093) | [10.6084/m9.figshare.28170555](https://doi.org/10.6084/m9.figshare.28170555) |
| SS-0094 | Collateral Damage | 11,000,000 | [cultivar-ss-0094](../../releases/tag/cultivar-ss-0094) | [10.6084/m9.figshare.28170558](https://doi.org/10.6084/m9.figshare.28170558) |
| SS-0095 | Extinction Protocol | 12,100,000 | [cultivar-ss-0095](../../releases/tag/cultivar-ss-0095) | [10.6084/m9.figshare.28170561](https://doi.org/10.6084/m9.figshare.28170561) |
| SS-0096 | D.N.R. (Do Not Resuscitate) | 13,100,000 | [cultivar-ss-0096](../../releases/tag/cultivar-ss-0096) | [10.6084/m9.figshare.28170564](https://doi.org/10.6084/m9.figshare.28170564) |

---

## Repository Structure

```
data/
  sequences/          ← All engineered construct FASTA files
  constructs/         ← construct_manifest.json (metadata for all 40 constructs)
  structures/         ← ColabFold PDB models, MSA .a3m files, PAE/scores JSON
  docking/            ← AutoDock Vina PDBQT results + docking box parameters
  md/                 ← NAMD MD simulation outputs (trajectory, energy, PDBs)
  analysis/           ← ESM2 scan results, blend designs, IFI scores
  sops/               ← HPLC quantification SOP, BSL-2 safety SOP
scripts/
  build_plan.py       ← Phase 1–7 pipeline build script
  phase1_gene_hunt.sh ← RNA-seq → DESeq2 → WGCNA pipeline
```

---

## Methods Summary

- **Gene hunting**: RNA-seq of *C. chinense* placenta; DESeq2 + WGCNA co-expression → 5 priority genes
- **Structure prediction**: ColabFold (AlphaFold2-PTM) for Pun1/AT3 and pAMT
- **ESM2 scanning**: Log-likelihood ratios across all Pun1 positions → stabilizing variants
- **Molecular docking**: AutoDock Vina 1.2.3, capsaicin + acyl chain + vanillylamine
- **MD simulation**: NAMD 3.0, CHARMM36m, explicit TIP3P water, 5000 steps NPT
- **Metabolic modeling**: COBRApy FBA for capsaicinoid, terpene, GABA, and glucosinolate pathways
- **CRISPR guides**: CHOPCHOP + manual off-target screening

---

## License

All data and documents are released under **CC BY 4.0**.

```bibtex
@article{IyengarFord2026_main,
  author  = {Iyengar Ford, Priyanca},
  title   = {Computational Design of Ten Engineered {\textit{Capsicum}} Cultivars
             Spanning 3--13\,M Scoville Heat Units},
  year    = {2026},
  doi     = {10.6084/m9.figshare.28170504}
}
```

**Platform DOI (OSF):** [10.17605/OSF.IO/69VB2](https://osf.io/69vb2/)  
**HuggingFace Dataset:** [scovillesplice/scoville-splice-capsaicinoid-data](https://huggingface.co/datasets/scovillesplice/scoville-splice-capsaicinoid-data)

---

*Scoville Splice · [scovillesplice.farm](https://scovillesplice.farm) · Platform launches October 31, 2026*
