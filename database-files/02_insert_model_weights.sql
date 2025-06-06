USE Consensus_DB; 

-- Insert model weights data
INSERT INTO ModelWeights (
    ModelName, DateAdded, Trade_union_density, Corporate_tax_rate, Education, Health, 
    Housing, Community_development, IRLT, Unemployment_rate, Population, GDP_per_capita, 
    Inflation, Region_East_Asia_and_Pacific, Region_Europe_and_Central_Asia, 
    Region_Latin_America_and_Caribbean, Region_Middle_East_and_North_Africa,
    Real_interest_rates, Productivity, Personal_property_tax
) VALUES (
    'Linear Regression', '2025-06-06', -0.0159021520556258, -0.0026577545776003, 
    0.0109177739952076, -0.0090514357657335, 0.0029934222437562, -0.0004333729544672, 
    0.0017525949705529, 0.0116903984566955, 0.0135502479286802, 0.0094281278634067, 
    0.0048602503451195, 0.3254217257270341, 0.3068476555189667, 0.4962985345068886, 
    0.381707490824724, 0.0, 0.0, 0.0
);

INSERT INTO ModelWeights (
    ModelName, DateAdded, Trade_union_density, Corporate_tax_rate, Education, Health, 
    Housing, Community_development, IRLT, Unemployment_rate, Population, GDP_per_capita, 
    Inflation, Region_East_Asia_and_Pacific, Region_Europe_and_Central_Asia, 
    Region_Latin_America_and_Caribbean, Region_Middle_East_and_North_Africa,
    Real_interest_rates, Productivity, Personal_property_tax
) VALUES (
    'Logistic Regression', '2025-06-06', -0.0730361071325626, -0.0127163156057952, 
    0.0482819027494454, -0.0360869170175761, 0.0126500444957124, -0.0015235252207348, 
    0.0102301189689968, 0.0570028898491497, 0.0635098572068014, 0.0453353570253226, 
    0.0243533912265543, -0.7351735028137188, -0.8198026929007239, -0.0260753255611929, 
    0.1234115098314789, 0.0, 0.0, 0.0
);

-- Insert prediction metrics data
INSERT INTO PredictMetrics (
    Metric, Trade_union_density, Corporate_tax_rate, Education, Health, Housing, 
    Community_development, IRLT, Unemployment_rate, Population, GDP_per_capita, 
    Inflation, Region_East_Asia_and_Pacific, Region_Europe_and_Central_Asia, 
    Region_Latin_America_and_Caribbean, Region_Middle_East_and_North_Africa,
    Real_interest_rates, Productivity, Personal_property_tax
) VALUES (
    'mean', 32.94699987125, 25.38490906, 0.0520058887554571, 0.0641270484977606, 
    0.0031681309922377, 0.0019377341312809, 3.4761538070153093, 7.925226652739379, 
    21704346.735, 40980.00975652196, 2.0690977327914903, 0.0, 0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0
);

INSERT INTO PredictMetrics (
    Metric, Trade_union_density, Corporate_tax_rate, Education, Health, Housing, 
    Community_development, IRLT, Unemployment_rate, Population, GDP_per_capita, 
    Inflation, Region_East_Asia_and_Pacific, Region_Europe_and_Central_Asia, 
    Region_Latin_America_and_Caribbean, Region_Middle_East_and_North_Africa,
    Real_interest_rates, Productivity, Personal_property_tax
) VALUES (
    'std', 21.85425264265921, 6.892238107873178, 0.0149060976336446, 0.0177205127042723, 
    0.0033088195536524, 0.0016875628037401, 2.254950538372162, 3.963356389732228, 
    26091837.308933742, 24369.87861567879, 1.9118575912416151, 0.0, 0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0
);
