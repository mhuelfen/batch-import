noun_noun_sims=../../../data/test_nn.csv
stat_stat_sims=../../../data/test_ss.csv
noun_stat=../../../data/test_ns.csv
# to filter out to low similarities
max_cos_dist=0.9
### make node files

# get all nouns
cut -f 1,2 $noun_noun_sims| tr "\t" "\n"  | sort | uniq | awk 'BEGIN { FS="\t";  OFS="\t"} {print $1,"Noun"}' > ../weltmodell_data/noun_nodes.csv

# get all statements
cut -f 1,2 $stat_stat_sims| tr "\t" "\n"  | sort | uniq | awk 'BEGIN { FS="\t";  OFS="\t"} {print $1,"Stat"}' > ../weltmodell_data/stat_nodes.csv

### make relationship files

# similarity rels
awk -v mcd=$max_cos_dist 'BEGIN { FS="\t";  OFS="\t";  } { if ($3 <= mcd) print $1,$2,"SIM_NOUN",$3}' $noun_noun_sims > ../weltmodell_data/noun_sim_rels.csv
awk -v mcd=$max_cos_dist 'BEGIN { FS="\t";  OFS="\t"} { if ($3 <= mcd) print $1,$2,"SIM_STAT",$3}' $stat_stat_sims  > ../weltmodell_data/stat_sim_rels.csv

# noun - statement rels
awk 'BEGIN { FS="\t";  OFS="\t"} {print $3,$4,"IN_STATE",$15}' $noun_stat > ../weltmodell_data/in_state_rels.csv

# get may be relations
awk 'BEGIN { FS="\t";  OFS="\t"} { if($3 ~ /} may be {/)  split($5,nouns,",")} END {print substr(nouns[1],2),substr(nouns[2],0,length(nouns[2])-1),"MAY_BE"}' $noun_stat > ../weltmodell_data/may_be_rels.csv


# add headers for batch import

