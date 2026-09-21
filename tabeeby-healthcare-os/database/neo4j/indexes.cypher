CREATE INDEX disease_name_idx FOR (d:Disease) ON (d.name);
CREATE INDEX drug_name_idx FOR (dr:Drug) ON (dr.name);
CREATE INDEX protein_name_idx FOR (p:Protein) ON (p.name);
CREATE INDEX gene_symbol_idx FOR (g:Gene) ON (g.symbol);
