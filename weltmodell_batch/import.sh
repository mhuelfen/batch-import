echo "Run in main directory sh sample/import.sh"
mvn test-compile exec:java -Dexec.mainClass="org.neo4j.batchimport.Importer" \
  -Dexec.args="weltmodell_batch/batch.properties target/weltmod_graph.db weltmodell_data/noun_nodes.csv,weltmodell_data/stat_nodes.csv weltmodell_data/noun_sim_rels.csv,weltmodell_data/stat_sim_rels.csv,weltmodell_data/in_state_rels.csv,weltmodell_data/may_be_rels.csv"