# -*- coding: utf-8 -*-


import pandas as pd
import os
from pathlib import Path
import numpy as np
import openpyxl

##### potřeba upravit si cestu k datům
data_path = Path('')
print(data_path)


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
    except Exception:
        print(num)
        return (False)


full_komplet = pd.DataFrame(
    columns=['Proces',
             'Podproces',
             'Aktivity',
             'PodAktivity',
             'Zdroj',
             'Kraj',
             'Čas',
             'Typ podání',
             'Role',
             'Čas - nekompletní žádost',
             'Čas - kompletní žádost',
             'ČETNOST',
             'POZNÁMKA',
             'Čas - nezadaná žádost - vložená do datové schránky',
             'Čas - částečně zadaná žádost',
             'Čas - úplně zadaná žádost'
             ]
)

kraje = os.listdir(data_path)
print(data_path)
for kraj in kraje:
    soubory_kraj = os.listdir(os.path.join(str(data_path), kraj))
    for soubor in soubory_kraj:
        komplet = pd.DataFrame(columns=full_komplet.columns)
        file_path = os.path.join(data_path, kraj, soubor)
        print(file_path)
        file_name = soubor
        xl = pd.ExcelFile(file_path)
        sheets = xl.sheet_names
        op_excel = xl.parse(sheets[0], header=1)
        op_excel.loc[op_excel['Proces'] == 'Proces']
        # pozice radku se slovem Proces
        list_of_subTables = op_excel.index[op_excel['Proces'] == 'Proces'].tolist()
        pocet_radku_celkem = len(op_excel)
        [(ind, list_of_subTables[list_of_subTables.index(ind) + 1] - 1)
         if ind != list_of_subTables[-1] else (ind, pocet_radku_celkem)
         for ind in list_of_subTables]

        # sloupec_fyzicky = [c for c in op_excel if op_excel[c].str.contains('Fyzicky podaná žádost').any()]
        # sloupec_datova_S = [c for c in op_excel if op_excel[c].str.contains('Datová schránka').any()]
        # sloupec_robot = [c for c in op_excel if op_excel[c].str.contains('Robot').any()]

        # sloupec_proces =  [c for c in op_excel if op_excel[c].str.contains('Proces').any()]
        op_excel['Proces'] = op_excel['Proces'].str.replace("P\s*\.\s*", "P ", regex=True)
        # op_excel['Proces'] = op_excel['Proces'].str.replace('P.', 'P ', regex=True)

        ##### prvni tabule priprava #####

        prv_T = op_excel.iloc[1:list_of_subTables[0] - 1, 0:]
        prv_T = prv_T.dropna(how='all', axis=0)
        prv_T['Název procesu'] = 'Podání žádosti'
        prv_T.rename(columns={'Fyzicky podaná žádost': 'Čas - nekompletní žádost_F',
                              'Datová schránka': 'Čas - nekompletní žádost_D',
                              'Robot': 'Čas - nezadaná žádost - vložená do datové schránky',
                              'Unnamed: 4': 'Čas - kompletní žádost_F',
                              'Unnamed: 5': 'ČETNOST',
                              'Unnamed: 6': 'POZNÁMKA_F',
                              'Unnamed: 7': 'Čas - nekompletní žádost_D',
                              'Unnamed: 8': 'Čas - kompletní žádost_D',
                              'Unnamed: 9': 'POZNÁMKA_D',
                              'Unnamed: 11': 'Čas - částečně zadaná žádost',
                              'Unnamed: 12': 'Čas - úplně zadaná žádost',
                              'Unnamed: 13': 'POZNÁMKA_R',
                              }, inplace=True)

        prv_T.insert(2, 'Podproces', '')
        prv_T['Podproces'] = prv_T[prv_T.Proces.str.contains('P\s*\d+\.', regex=True, na=False)]['Proces'].dropna()
        prv_T.insert(4, 'PodAktivity', '')
        prv_T['PodAktivity'] = prv_T['Aktivity']

        for p in list(prv_T[~prv_T.Proces.str.contains('P\s*\d+\.', regex=True, na=False)]['Proces'].dropna()):
            aktivita = list(prv_T.loc[prv_T['Proces'] == p]['Aktivity'])[0]
            prv_T.loc[prv_T.Proces.str.contains('P\s*\d+\.', regex=True, na=False), 'Aktivity'] = aktivita
            prv_T['Proces'] = prv_T['Proces'].str.replace(p + '\..*', p, regex=True)

        prv_T.loc[prv_T.Aktivity == prv_T.PodAktivity, 'PodAktivity'] = np.nan
        prv_T = prv_T[~prv_T['Proces'].isna() | ~prv_T['Podproces'].isna() | ~prv_T['Aktivity'].isna()]
        prv_T = prv_T[prv_T['Aktivity'] != "Celkový čas (minuty)"]

        ####TODO select sloupcu podle nazvu a ne podle indexu
        #####fyzicky podana zadost #####
        fyz_z = prv_T[
            ['Název procesu', 'Proces', 'Podproces', 'Aktivity', 'PodAktivity', 'Role', 'Čas - nekompletní žádost_F',
             'Čas - kompletní žádost_F', 'ČETNOST',
             'POZNÁMKA_F']].copy()
        fyz_z['Typ podání'] = 'Fyzicky podaná žádost'
        fyz_z = fyz_z.rename(columns={'Čas - nekompletní žádost_F': 'Čas - nekompletní žádost',
                                      'Čas - kompletní žádost_F': 'Čas - kompletní žádost',
                                      'POZNÁMKA_F': 'POZNÁMKA'})

        #####Datová schránka #####
        dat_z = prv_T[
            ['Název procesu', 'Proces', 'Podproces', 'Aktivity', 'PodAktivity', 'Role', 'Čas - nekompletní žádost_D',
             'Čas - kompletní žádost_D',
             'POZNÁMKA_D']].copy()
        dat_z['Typ podání'] = 'Datová schránka'
        dat_z = dat_z.rename(columns={'Čas - nekompletní žádost_D': 'Čas - nekompletní žádost',
                                      'Čas - kompletní žádost_D': 'Čas - kompletní žádost',
                                      'POZNÁMKA_D': 'POZNÁMKA'})

        #####Robot #####
        rob_z = prv_T[['Název procesu', 'Proces', 'Podproces', 'Aktivity', 'PodAktivity', 'Role',
                       'Čas - nezadaná žádost - vložená do datové schránky',
                       'Čas - částečně zadaná žádost', 'Čas - úplně zadaná žádost',
                       'POZNÁMKA_R']].copy()
        rob_z['Typ podání'] = 'Robot'
        rob_z = rob_z.rename(columns={'POZNÁMKA_R': 'POZNÁMKA'})

        komplet = pd.concat([komplet, fyz_z, dat_z, rob_z], ignore_index=True)
        ###################

        druha_T = op_excel.iloc[list_of_subTables[0] - 1:list_of_subTables[1] - 1, 0:]

        nazev_proc = druha_T.iloc[0, 1]
        druha_T = druha_T.dropna(how='all', axis=0)
        druha_T = druha_T[druha_T['Aktivity'] != "Celkový čas (minuty)"]
        druha_T = druha_T.rename(columns=druha_T.iloc[1])
        druha_T = druha_T.iloc[2:, :]
        druha_T = druha_T.rename(columns={'P oces': 'Proces'})
        druha_T = druha_T[['Proces', 'Aktivity', 'Role', 'POZNÁMKA', 'Čas']]
        druha_T['Název procesu'] = nazev_proc
        druha_T = druha_T.dropna(how='all', axis=1)
        komplet = pd.concat([komplet, druha_T], ignore_index=True)
        ##################
        treti_T = op_excel.iloc[list_of_subTables[1] - 1:list_of_subTables[2] - 1, 0:]
        treti_T = treti_T.replace('', np.nan, regex=False)
        treti_T = treti_T.replace(' ', np.nan, regex=False)
        nazev_proc = treti_T.iloc[0, 1].strip()
        treti_T = treti_T.dropna(how='all', axis=0)

        treti_T = treti_T.rename(columns=treti_T.iloc[1])
        treti_T = treti_T.iloc[2:, :]
        treti_T = treti_T.rename(columns={'P oces': 'Proces'})
        treti_T.insert(0, 'Název procesu', nazev_proc)
        aktivity_name = treti_T.iloc[0, 2]
        treti_T.iloc[0, 0:5] = treti_T.columns[0:5]
        treti_T = treti_T.dropna(how='all', axis=1)
        treti_T.iloc[0, 4] = treti_T.iloc[0, 4].replace(" -", " - ").replace("  ", " ")
        treti_T.iloc[0, 5] = treti_T.iloc[0, 5].replace(" -", " - ").replace("  ", " ") + '_F'
        treti_T.iloc[0, 6] = treti_T.iloc[0, 6].replace(" -", " - ").replace("  ", " ") + '_F'
        treti_T.iloc[0, 7] = treti_T.iloc[0, 7].replace(" -", " - ").replace("  ", " ") + '_F'
        treti_T.iloc[0, 8] = treti_T.iloc[0, 8].replace(" -", " - ").replace("  ", " ") + '_D'
        treti_T.iloc[0, 9] = treti_T.iloc[0, 9].replace(" -", " - ").replace("  ", " ") + '_D'
        treti_T.iloc[0, 10] = treti_T.iloc[0, 10].replace(" -", " - ").replace("  ", " ") + '_D'
        treti_T.iloc[0, 11] = treti_T.iloc[0, 11].replace(" -", " - ").replace("  ", " ")
        treti_T.iloc[0, 12] = treti_T.iloc[0, 12].replace(" -", " - ").replace("  ", " ")
        treti_T.iloc[0, 13] = treti_T.iloc[0, 13].replace(" -", " - ").replace("  ", " ")
        treti_T.iloc[0, 14] = treti_T.iloc[0, 14].replace(" -", " - ").replace("  ", " ") + '_R'
        treti_T.columns = treti_T.iloc[0]
        treti_T = treti_T.iloc[1:, :]
        treti_T = treti_T.rename(
            columns={'Čas - nezadaná žádost - vložená do DS': 'Čas - nezadaná žádost - vložená do datové schránky'})
        treti_T = treti_T[treti_T['Aktivity'] != "Celkový čas (minuty)"]
        #####fyzicky podana zadost #####
        fyz_z = treti_T[['Název procesu', 'Proces', 'Aktivity', 'Role', 'Čas - nekompletní žádost_F',
                         'Čas - kompletní žádost_F', 'POZNÁMKA_F']].copy()
        fyz_z['Typ podání'] = 'Fyzicky podaná žádost'
        fyz_z = fyz_z.rename(columns={'Čas - nekompletní žádost_F': 'Čas - nekompletní žádost',
                                      'Čas - kompletní žádost_F': 'Čas - kompletní žádost',
                                      'POZNÁMKA_F': 'POZNÁMKA'})

        #####Datová schránka #####
        dat_z = treti_T[['Název procesu', 'Proces', 'Aktivity', 'Role', 'Čas - nekompletní žádost_D',
                         'Čas - kompletní žádost_D',
                         'POZNÁMKA_D']].copy()
        dat_z['Typ podání'] = 'Datová schránka'
        dat_z = dat_z.rename(columns={'Čas - nekompletní žádost_D': 'Čas - nekompletní žádost',
                                      'Čas - kompletní žádost_D': 'Čas - kompletní žádost',
                                      'POZNÁMKA_D': 'POZNÁMKA'})
        # treti_T.columns

        #####Robot #####
        rob_z = treti_T[
            ['Název procesu', 'Proces', 'Aktivity', 'Role', 'Čas - nezadaná žádost - vložená do datové schránky',
             'Čas - částečně zadaná žádost', 'Čas - úplně zadaná žádost',
             'POZNÁMKA_R']].copy()
        rob_z['Typ podání'] = 'Robot'
        rob_z = rob_z.rename(columns={'POZNÁMKA_R': 'POZNÁMKA'})

        komplet = pd.concat([komplet, fyz_z, dat_z, rob_z], ignore_index=True)
        #################

        ctvrta_T = op_excel.iloc[list_of_subTables[2] - 1:, 0:]
        nazev_proc = ctvrta_T.iloc[0, 1]
        ctvrta_T = ctvrta_T.dropna(how='all', axis=0)
        ctvrta_T = ctvrta_T[ctvrta_T['Aktivity'] != "Celkový čas (minuty)"]
        ctvrta_T = ctvrta_T.rename(columns=ctvrta_T.iloc[1])
        ctvrta_T = ctvrta_T.iloc[2:, :]
        ctvrta_T = ctvrta_T.rename(columns={'P oces': 'Proces'})
        ctvrta_T = ctvrta_T[['Proces', 'Aktivity', 'Role', 'POZNÁMKA', 'Čas', 'ČETNOST']]
        ctvrta_T['Název procesu'] = nazev_proc
        ctvrta_T = ctvrta_T.dropna(how='all', axis=1)
        komplet = pd.concat([komplet, ctvrta_T], ignore_index=True)
        komplet['Zdroj'] = file_name
        komplet['Kraj'] = kraj
        full_komplet = pd.concat([full_komplet, komplet], ignore_index=True)

full_komplet = full_komplet.applymap(lambda x: x.strip() if isinstance(x, str) else x)

numeric_cols = ['Čas',
                'Čas - nekompletní žádost',
                'Čas - kompletní žádost',
                'Čas - nezadaná žádost - vložená do datové schránky',
                'Čas - částečně zadaná žádost',
                'Čas - úplně zadaná žádost']
full_komplet = full_komplet.replace('', np.nan)

for col in numeric_cols:
    full_komplet[full_komplet[col].apply(lambda x: not isfloat(x))] = np.nan
    if len(full_komplet[full_komplet[col].apply(lambda x: not isfloat(x))]) > 0:
        print(col)

full_komplet = full_komplet.loc[~pd.isna(full_komplet['Proces'])].reset_index(drop=True)
full_komplet.to_excel("full_data.xlsx", index=False)

# zdroj pro analyzu ve word cloudu na poznamky od vyplnovatelu
df_poznamky = full_komplet \
    .value_counts(subset=['Zdroj', 'Proces', 'POZNÁMKA']) \
    .to_frame() \
    .rename(columns={0: 'Pocet'})

# df_poznamky.rename(columns={'0': 'count'})
df_poznamky.to_excel("df_poznamky.xlsx", merge_cells=False)

full_komplet_v2 = pd.DataFrame(
    columns=['Proces',
             'Podproces',
             'Aktivity',
             'PodAktivity',
             'Zdroj',
             'Kraj',
             'Čas',
             'Typ podání',
             'Role',
             'Název procesu',
             'Typ žádosti']
)
full_komplet_v3 = full_komplet_v2.copy()

male_tabulky = full_komplet.loc[pd.notna(full_komplet['Čas'])][['Proces',
                                                                'Podproces',
                                                                'Aktivity',
                                                                'PodAktivity',
                                                                'Zdroj',
                                                                'Kraj',
                                                                'Čas',
                                                                'Typ podání',
                                                                'Role',
                                                                'Název procesu']]
male_tabulky['Typ žádosti'] = np.nan

full_komplet_v2 = pd.concat([full_komplet_v2, male_tabulky])
full_komplet_v3 = pd.concat([full_komplet_v3, male_tabulky])

cas_cols = ['Čas - nekompletní žádost',
            'Čas - kompletní žádost',
            'Čas - nezadaná žádost - vložená do datové schránky',
            'Čas - částečně zadaná žádost', 'Čas - úplně zadaná žádost']

for c in cas_cols:
    new_c = c.replace("Čas - ", "")
    v1 = full_komplet.loc[(~pd.notna(full_komplet['Čas'])) & (pd.notna(full_komplet[c]))][['Proces',
                                                                                           'Podproces',
                                                                                           'Aktivity',
                                                                                           'PodAktivity',
                                                                                           'Zdroj',
                                                                                           'Kraj',
                                                                                           'Čas',
                                                                                           'Typ podání',
                                                                                           'Role',
                                                                                           'Název procesu',
                                                                                           c]]
    print(len(v1))
    v1['Čas'] = v1[c]
    v1['Typ žádosti'] = new_c
    v1 = v1.drop(c, axis=1)
    full_komplet_v2 = pd.concat([full_komplet_v2, v1])
full_komplet_v2 = full_komplet_v2.rename(columns={'Čas': 'Cas',
                                                  'Typ podání': 'Typ podani',
                                                  'Název procesu': 'Nazev procesu',
                                                  'Typ žádosti': 'Typ zadosti'})
full_komplet_v2.to_excel("full_data_v2.xlsx", index=False)

for c in cas_cols:
    new_c = c.replace("Čas - ", "")
    v1 = full_komplet.loc[~pd.notna(full_komplet['Čas'])][['Proces',
                                                           'Podproces',
                                                           'Aktivity',
                                                           'PodAktivity',
                                                           'Zdroj',
                                                           'Kraj',
                                                           'Čas',
                                                           'Typ podání',
                                                           'Role',
                                                           'Název procesu',
                                                           c]]
    print(len(v1))
    v1['Čas'] = v1[c]
    v1['Typ žádosti'] = new_c
    v1 = v1.drop(c, axis=1)
    full_komplet_v3 = pd.concat([full_komplet_v3, v1])
full_komplet_v3 = full_komplet_v3.rename(columns={'Čas': 'Cas',
                                                  'Typ podání': 'Typ podani',
                                                  'Název procesu': 'Nazev procesu',
                                                  'Typ žádosti': 'Typ zadosti'})

full_komplet_v3 = full_komplet_v3.loc[~pd.isna(full_komplet_v3['Proces'])].reset_index(drop=True)
full_komplet_v2 = full_komplet_v2.loc[~pd.isna(full_komplet_v2['Proces'])].reset_index(drop=True)
full_komplet_v3.to_excel("full_data_v3.xlsx", index=False)
full_komplet_v2.to_excel("full_data_v2.xlsx", index=False)

