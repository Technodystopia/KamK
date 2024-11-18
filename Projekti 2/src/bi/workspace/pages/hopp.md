---
title: Hopp Asiakaspalautteet
description: Visualisointi AIKTEHOHO, EALAPSAIK ja ENSIHOITO yksikköjen asiakaspalautteiden jakaumasta.
layout: page
---

<Details title='Asiakaspalautteiden analyysi'>
    Tässä raportissa tarkastellaan AIKTEHOHO, EALAPSAIK ja ENSIHOITO yksikköjen asiakaspalautteiden jakaumaa kysymyskohtaisesti saatavilla olleilta vuosineljänneksiltä.
</Details>

```hopp_orig_gold
select * from warehouse.hopp_orig_gold
```

<Details title='Visualisointi: Yksikköjen A, B ja C kysymyskohtaiset vastaukset'>
    Visualisointi näyttää yksiköiden A, B ja C kaikkien kysymysten vastausten jakaumat saatavilla olevilta vuosineljänneksiltä.
</Details>

```hopp_unit_feedback_distribution
select yksikkokoodi, kvartaali_vuosi, kysymys, vastaus, count(*) as vastausten_maara
from (
    select yksikkokoodi, kvartaali_vuosi, 'value1' as kysymys, value1 as vastaus from warehouse.hopp_orig_gold
    union all
    select yksikkokoodi, kvartaali_vuosi, 'value2' as kysymys, value2 as vastaus from warehouse.hopp_orig_gold
    -- Lisää unionit jokaiselle valueX-sarakkeelle
    union all
    select yksikkokoodi, kvartaali_vuosi, 'value22' as kysymys, value22 as vastaus from warehouse.hopp_orig_gold
) as kysymykset
where yksikkokoodi in ('A', 'B', 'C')
group by yksikkokoodi, kvartaali_vuosi, kysymys, vastaus
order by yksikkokoodi, kvartaali_vuosi, kysymys, vastaus;

```

<BarChart
    data={hopp_unit_feedback_distribution}
    x='kysymys' y='vastausten_maara'
    series='yksikkokoodi'
    groupBy='vastaus'
    title='Yksikköjen A, B ja C asiakaspalautteiden jakauma kysymyksittäin' />

<DataTable data={hopp_orig_gold}/>
