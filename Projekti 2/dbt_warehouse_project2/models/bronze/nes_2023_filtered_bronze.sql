{{ config(materialized='table') }}

WITH source AS (
    SELECT
        CAST("Yksikkökoodi" AS VARCHAR) AS yksikkokoodi,
        COALESCE(CAST("Työnkuva" AS INTEGER), 0) AS value1,
        COALESCE(CAST("Työsuhde" AS INTEGER), 0) AS value2,
        COALESCE(CAST("Koulutus" AS INTEGER), 0) AS value3,
        COALESCE(CAST("Työvuoro" AS INTEGER), 0) AS value4,
        COALESCE(CAST("Työsuhteen_pituus" AS INTEGER), 0) AS value5,
        COALESCE(CAST("Uskon_org_päämääriin" AS INTEGER), 0) AS value6,
        COALESCE(CAST("Tiedän_oman_toim_org_päämääriin" AS INTEGER), 0) AS value7,
        COALESCE(CAST("Org_johto_arvojen_muk" AS INTEGER), 0) AS value8,
        COALESCE(CAST("Hoitajat_taitavia" AS INTEGER), 0) AS value9,
        COALESCE(CAST("Hoitajat_NPT_käyttöön" AS INTEGER), 0) AS value10,
        COALESCE(CAST("Noudatan_NP_toimohjeita" AS INTEGER), 0) AS value11,
        COALESCE(CAST("Aktiivisesti_osallistan_pot" AS INTEGER), 0) AS value12,
        COALESCE(CAST("Työsuojelu_toimii" AS INTEGER), 0) AS value13,
        COALESCE(CAST("Org_apua_työuupumukseen" AS INTEGER), 0) AS value14,
        COALESCE(CAST("Mahdoll_seurata_hoitotyön_tuloksia" AS INTEGER), 0) AS value15,
        COALESCE(CAST("Osall_päivittäisjohtamisen_kokouksiin" AS INTEGER), 0) AS value16,
        COALESCE(CAST("Lähiesimies_avoin_ehdotuksille" AS INTEGER), 0) AS value17,
        COALESCE(CAST("Lähiesimies_hlökunnan_puolestapuhuja" AS INTEGER), 0) AS value18,
        COALESCE(CAST("Lähiesimies_korostaa_hoidon_laatua" AS INTEGER), 0) AS value19,
        COALESCE(CAST("Lähiesimies_hoitaa_velvoll" AS INTEGER), 0) AS value20,
        COALESCE(CAST("Jyh_edustaa_ht_näkyvästi" AS INTEGER), 0) AS value21,
        COALESCE(CAST("Org_huomioi_hoitajien_ehd" AS INTEGER), 0) AS value22,
        COALESCE(CAST("Kiitosta_työstä" AS INTEGER), 0) AS value23,
        COALESCE(CAST("Suor_arv_suht_selk_tav" AS INTEGER), 0) AS value24,
        COALESCE(CAST("Säännöllinen_palaute" AS INTEGER), 0) AS value25,
        COALESCE(CAST("Vaikutan_pothoidon_suu_ja_tot" AS INTEGER), 0) AS value26,
        COALESCE(CAST("Sopivasti_itsenäinen" AS INTEGER), 0) AS value27,
        COALESCE(CAST("Osall_päätöksiin_työ" AS INTEGER), 0) AS value28,
        COALESCE(CAST("Org_arvostaa_hoitajien_työpanosta" AS INTEGER), 0) AS value29,
        COALESCE(CAST("Lääkärit_arvostavat_hoitajia" AS INTEGER), 0) AS value30,
        COALESCE(CAST("Osall_lääk_kanssa_pothoidon_päät" AS INTEGER), 0) AS value31,
        COALESCE(CAST("Org_ei_hyv_loukk_käytöstä" AS INTEGER), 0) AS value32,
        COALESCE(CAST("Puheeksi_epäkohdat_lääkärit" AS INTEGER), 0) AS value33,
        COALESCE(CAST("Puheeksi_epäkohdat_hoitajat" AS INTEGER), 0) AS value34,
        COALESCE(CAST("Oma_aloitteisti_apua" AS INTEGER), 0) AS value35,
        COALESCE(CAST("Asiantuntijan_konsultointi" AS INTEGER), 0) AS value36,
        COALESCE(CAST("Ristiriitojen_reilu_ratk" AS INTEGER), 0) AS value37,
        COALESCE(CAST("Keskustelut_pothoidon_kehitt" AS INTEGER), 0) AS value38,
        COALESCE(CAST("Tiedän_miten_suor_paremmin" AS INTEGER), 0) AS value39,
        COALESCE(CAST("Mahdoll_keskusteluun_ammuralla_eten" AS INTEGER), 0) AS value40,
        COALESCE(CAST("Amm_kasvu_merkittävää" AS INTEGER), 0) AS value41,
        COALESCE(CAST("Opiskelua_tuetaan" AS INTEGER), 0) AS value42,
        COALESCE(CAST("Org_tarjoaa_urallakehitt_mahd" AS INTEGER), 0) AS value43,
        COALESCE(CAST("Käytettävissä_tarv_laitteet" AS INTEGER), 0) AS value44,
        COALESCE(CAST("Sopivasti_potilaita" AS INTEGER), 0) AS value45,
        COALESCE(CAST("Riittävästi_aikaa_pot" AS INTEGER), 0) AS value46,
        COALESCE(CAST("Ei_pyydetty_tekemään_haitall_pot" AS INTEGER), 0) AS value47,
        COALESCE(CAST("Org_tukee_hoitajien_työtä_menetelmät" AS INTEGER), 0) AS value48,
        COALESCE(CAST("Tietoa_org_suu_ja_tav" AS INTEGER), 0) AS value49,
        COALESCE(CAST("Hyvät_suhteet_hoitajiin" AS INTEGER), 0) AS value50,
        COALESCE(CAST("Tukea_avustavalta_hlökunnalta" AS INTEGER), 0) AS value51,
        COALESCE(CAST("Vaikutan_työvuorojen_suunn" AS INTEGER), 0) AS value52,
        COALESCE(CAST("Pot_vuorovaikutus_mielekästä" AS INTEGER), 0) AS value53,
        COALESCE(CAST("Ylpeä_ammatistani" AS INTEGER), 0) AS value54,
        COALESCE(CAST("Suosittelen_org" AS INTEGER), 0) AS value55,
        COALESCE(CAST("Org_innostaa" AS INTEGER), 0) AS value56,
        COALESCE(CAST("Työskentelen_3v_todnäk" AS INTEGER), 0) AS value57,
        COALESCE(CAST("Valmis_panostamaan" AS INTEGER), 0) AS value58
    FROM read_csv_auto('../data/lake/staging/CSV/nes/filtered/nes_2024_filtered.csv')
    WHERE "Yksikkökoodi" IN ('AIKTEHOHO', 'EALAPSAIK', 'ENSIHOITO')
)

SELECT
    REGEXP_REPLACE(yksikkokoodi, 'ENSIHOITO|EALAPSAIK|AIKTEHOHO', 
        CASE 
            WHEN yksikkokoodi = 'ENSIHOITO' THEN 'A'
            WHEN yksikkokoodi = 'EALAPSAIK' THEN 'B'
            WHEN yksikkokoodi = 'AIKTEHOHO' THEN 'C'
        END
    ) AS yksikkokoodi,
    {% for i in range(1, 59) %}
        value{{ i }}{% if not loop.last %},{% endif %}
    {% endfor %}
FROM source
