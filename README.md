# FluStAR
Flu subtyping and assembly resource

## Contents
This repo is still under active development. Current contents include sketches for all 8 genome segments and scripts for screening read sets against the H and N segments and to produce a report identifying the subtype from this information. Additional tools to screen against all 8 segements and produce a composite reference based assembly based on these matches are coming soon. 

## Installation and usage instructions
Coming Soon

## A bit on methods
All non-redundant sequences for each segment were downloaded from NCBI's Influenza Virus Database. Sequences were then clustered at 95% identity using CD-Hit-est. Representative sequences for each segment were filtered based on length to exclude aberrant sequences for each segment. For the H and N segments, clusters were screened to check whether the representative sequence for each cluster was the same type as the majority of sequences in that cluster. If not, it was replaced with a different sequence that was labeled as the majority type. Trees were then constructed from all representative sequences for these two segments to verify that each subtype clustered together. 
