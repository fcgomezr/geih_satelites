
import pandas as pd
import numpy as np

class MT_job:

    
    def print_pop_empl(df, year):
        """
        Imprime la población y la ocupación para el año especificado.

        Args:

        df: El conjunto de datos a utilizar.
        year: El año para el que se desea imprimir los datos.

        Returns:

        Ninguno.
        """
        if year < 2021:
            print(
                "Población fex_2005 :", round(df['FEX_C_2011'].sum() / 12, 0),
                "Población fex_2018 :", round(df['FEX_C18'][df.MES >= 1].sum() / 12, 0), "\n",
                "Ocupados fex_2005 :", round(df['FEX_C_2011'][df.OCI == 1].sum() / 12, 0),
                "Ocupados fex_2018 :", round(df['OCI_FEX18_2'][df.MES >= 1].sum() / 12, 0))
        else:
            print(
                "Población fex_2018 :", round(df['FEX_C18'].sum() / 12, 0),"\n",
                "Ocupados fex_2018 :", round(df['FEX_C18'][df.OCI == 1].sum() / 12, 0),"\n",
                "Puestos de trabajo :", round(df[['Puestos','MES']][df.OCI == 1].groupby(['MES']).sum().mean())
            )   

    def new_vars(df):
        """
        Crea las columnas de horas trabajadas, horas efectivas, horas efectivas anuales, puestos y categoría de ocupación.

        Args:
            df: El DataFrame de datos del GEIH.

        Returns:
            El DataFrame con las columnas agregadas.
        """

        df['fex'] = df['FEX_C18']
        df['hor'] = df['P6850'] * df['fex'] # Horas trabajadas
        df['horas_efectivas'] = df['fex'] * df['P6850'] # Horas efectivas
        df['horas_efectivas_anuales'] = df['horas_efectivas'] * 52 # Horas efectivas anuales
        df['Puestos'] = df['fex'] * df['P6850'] / (48) # Puestos
        df['cat_ocup'] = df['P6430'].apply(lambda x: 'Asalariado' if x in [1, 2, 3, 8] else (
            'Independiente' if x in [4, 5, 6, 7, 9] else 'nan')) # Categoría de ocupación
        df['asal_hours'] = df.horas_efectivas.where(df.cat_ocup == 'Asalariado', ) # Horas efectivas asalariados
        df['ind_hours'] = df.horas_efectivas.where(df.cat_ocup == 'Independiente', ) # Horas efectivas independientes
        df['asal'] = df.fex.where(df.cat_ocup == 'Asalariado', ) # Fex asalariados
        df['ind'] =df.fex.where(df.cat_ocup == 'Independiente', ) # Fex independientes

        return df
    def pivot(db,index,columns,name):
        """
        Calcula una pivot table de un DataFrame de pandas.

        Args:
            db: Un DataFrame de pandas.
            index: Una lista de columnas que se utilizarán como índice de la pivot table.
            columns: Una lista de columnas que se utilizarán como columnas de la pivot table.
            values: Una lista de columnas que se utilizarán como valores de la pivot table.
            name: El nombre de la columna de valores de la pivot table.

        Returns:
            Un DataFrame con la pivot table calculada.
        """

        dr = pd.pivot_table(db[(db['OCI']==1) & (db['P6400']==2) & (db['P6410']==1) | 
                               (db['P6410']==2) |(db['P6410']==3) & (db['RAMA4D_R4']!='')],
                            values=[name],
                            index=index,columns=columns,
                            aggfunc={name: [sum]})
        dr = dr.groupby(axis=1, level=(2,3)).mean()

        drr = pd.pivot_table(db[(db['OCI']==1) & (db['P6400']==2) &  (db['P6410']==4)| 
                                db.P6410.isnull()  & (db['RAMA4D_R4']!='')], 
                             values=[name],
                             index=index,columns=columns,
                             aggfunc={name: [sum]})
        drr = drr.groupby(axis=1, level=(2,3)).mean()
        drr.loc['M + N'] = dr.sum(numeric_only=True, axis=0) + drr.filter(like='M + N', axis=0).sum(numeric_only=True, axis=0)

        drr=pd.DataFrame(drr.to_records())
        drr.columns = [hdr.replace("(", "").replace(")", "").replace("'sum'","").replace(",","").replace("'","")\
                             for hdr in drr.columns]
        return drr

    def table_second(df):
        """
        Calcula las horas trabajadas por segunda ocupación y los puestos de trabajo por segunda ocupación.

        Args:
         df: DataFrame con los datos de la encuesta.

        Returns:
         df: DataFrame con las horas trabajadas por segunda ocupación y los puestos de trabajo por segunda ocupación.
       """
        # Calcula las horas trabajadas por segunda ocupación

        df['Horas_2empl'] = df['fex'] * df['P7045']

        # Calcula los puestos de trabajo por segunda ocupación
        df['PuestosEmp2'] = df['Horas_2empl'] / 48

        return df

    def table_output(dff_1, dff_2,name):
        """
      Calcula los promedios de horas semanales trabajadas a la semana, las horas anuales trabajadas del trabajo principal por actividad económica y categoría ocupacional y el coeficiente de ajuste del trabajo principal por actividad económica y categoría ocupacional.

      Args:
        dff_1: Tabla MT con horas efectivas de trebajos.
        dff_2: Tabla MT con población ocupada.
        name : El nombre de la columna de valores de la pivot table.

      Returns:
        dff_3: DataFrame con los promedios de horas semanales trabajadas a la semana.
        dff_4: DataFrame con las horas anuales trabajadas del trabajo principal por actividad económica y categoría ocupacional.
        dff_5: DataFrame con el coeficiente de ajuste del trabajo principal por actividad económica y categoría ocupacional.
      """

      # Calcula los promedios de horas semanales trabajadas a la semana
        dff_3 = pd.DataFrame(dff_1[name])
        dff_3['PrAsHourH'], dff_3['PrAsHourM'] = dff_1['Asalariado 1'] / dff_2['Asalariado 1'], dff_1['Asalariado 2'] / dff_2['Asalariado 2']
        dff_3['PrInHourH'], dff_3['PrInHourM'] = dff_1['Independiente 1'] / dff_2['Independiente 1'], dff_1['Independiente 2'] / dff_2['Independiente 2']

      # Calcula las horas anuales trabajadas del trabajo principal por actividad económica y categoría ocupacional

        dff_4 = dff_1[['Asalariado 1', 'Asalariado 2', 'Independiente 1', 'Independiente 2']] * 52 / 1e6

      # Calcula el coeficiente de ajuste del trabajo principal por actividad económica y categoría ocupacional

        dff_5 = dff_3[['PrAsHourH', 'PrAsHourM', 'PrInHourH', 'PrInHourM']] / 48
        return dff_3, dff_4, dff_5

    def pivot_sec(dff_csa, dff_csi, df,var):
        """
      Calcula los pesos de las actividades económicas y las categorías ocupacionales, utilizando las variables `dff_csa` y `dff_csi`.

      Args:
        dff_csa: DataFrame con las horas trabajadas por semana por actividad económica.
        dff_csi: DataFrame con las horas trabajadas por semana por categoría ocupacional.
        df: DataFrame con los datos de la encuesta.
        var : PH para horas trabajadas ; P para personas

      Returns:
        df: DataFrame con los pesos de las actividades económicas y las categorías ocupacionales.
        """


        if var == "P":
        # Calcula los pesos poblacionales
            df["PAsal"] = df["PerAsal_2005"] / sum(df["PerAsal_2005"])
            df["PInd"] = df["PerInd_2005"] / sum(df["PerInd_2005"])
        elif var == "PH":
        # Calcula los pesos poblacionales en horas
            df["PHAsal"] = (df["HorAsal_2005"] * df["PerAsal_2005"]) / sum(df["HorAsal_2005"] * df["PerAsal_2005"])
            df["PHInd"] = (df["HorAsal_2005"] * df["PerInd_2005"]) / sum(df["HorAsal_2005"] * df["PerInd_2005"])
        else:
        # Error si el tipo de peso no es válido
            raise ValueError("El tipo de peso debe ser 'P' o 'PH'")

        name_i = f"{var}Ind"
        name_a = f"{var}Asal"

        name1 = f"{name_a}H"
        name2 = f"{name_a}M"
        name3 = f"{name_i}H"
        name4 = f"{name_i}M"

      # Calcula el peso de la actividad económica en horas
        df[name1] = df[name_a] * dff_csa[1]

      # Calcula el peso de la actividad económica en meses
        df[name2] = df[name_a] * dff_csa[2]

      # Calcula el peso de la categoría ocupacional en horas
        df[name3] = df[name_i] * dff_csi[1]

      # Calcula el peso de la categoría ocupacional en meses
        df[name4] = df[name_i] * dff_csi[2]

        return df
    def pon_sec(Pond,PondH,d):
        """
        Crea una función a partir de un diccionario de ramas.

        Args:
        d: Diccionario de ramas.

        Returns:
        Función que calcula las proporciones de gastos de personal y materiales por rama.
        """

        # Crea un DataFrame con las ramas como índice.
        PondST = pd.DataFrame(d, index=d['Ramas'])

        # Calcula las proporciones de gastos de personal.
        PondST['AsalH'] = PondH['PHAsalH'] / Pond['PAsalH']
        PondST['AsalM'] = PondH['PHAsalM'] / Pond['PAsalM']

        # Calcula las proporciones de gastos de materiales.
        PondST['IndH'] = PondH['PHIndH'] / Pond['PIndH']
        PondST['IndM'] = PondH['PHIndM'] / Pond['PIndH']

        # Calcula las proporciones totales de gastos de personal y materiales.
        PondST['TAsalH'] = (PondH['PHAsalH'] + PondH['PHAsalM']) / (Pond['PAsalH'] + Pond['PAsalM'])
        PondST['TIndH'] = (PondH['PHIndH'] + PondH['PHIndM']) / (Pond['PIndH'] + Pond['PIndM'])
        PondST['TGIndH'] = (PondH['PHAsalH'] + PondH['PHAsalM'] + PondH['PHIndH'] + PondH['PHIndM']) / (Pond['PIndH'] + Pond['PIndM'] + Pond['PAsalH'] + Pond['PAsalM'])

        return PondST
    def pivot_none(df, column_name):
        """
        Converts the given column in the given DataFrame to numeric type and calculates
        new column values using the given formula.

        Args:
        df: Pandas DataFrame.
        column_name: Name of the column to convert and calculate new values for.

        Returns:
        Pandas DataFrame with the new column.
        """

        # Convert the column to numeric type.
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

        # Calculate the new column values.
        df['P7480S1A1e'] = df['fex'] * df['P3095S1']*df['P3095S2']/12
        df['P7480S7e']   = df['fex'] * df['P3092S1']*df['P3092S2']/12
        df['P7480S9e']   = df['fex'] * df['P3098S1']*df['P3098S2']/12
        df['P7480S10e']  = df['fex'] * df['P3099S1']*df['P3099S2']/12

        return df
    def calculate_NoRen_1(df):
        """
        Calculates the NoRen_1 DataFrame for the given DataFrame.

        Args:
        df: Pandas DataFrame.

        Returns:
        Pandas DataFrame with the NoRen_1 columns.
        """
        # Create the NoRen_1 DataFrame.
        d = {'Ramas' : ['A','B','C','D + E','F','G + H + I', 'J','K','L','M + N','O + P + Q','R + S + T'],
        'PerH':[0] * 12,'PerM':[0] * 12,'HourH':[0] * 12,'HourM':[0] * 12}
        NoRen_1= pd.DataFrame(d,index=d['Ramas'])
        # Calculate the new column values.
        df['fex'] = df['fex']/12 
        fr1 = df['fex'][df['P3095'] == 1].groupby(df['P3271']).sum()
        fr2 = df['fex'][df['P3092'] == 1].groupby(df['P3271']).sum()
        fr3 = (df['fex'][df['P3098'] == 1].groupby(df['P3271']).sum() +
              df['fex'][df['P3099'] == 1].groupby(df['P3271']).sum())

        fr4 = df['P7480S1A1e'][df['P3095'] == 1].groupby(df['P3271']).sum()
        fr5 = df['P7480S7e'][df['P3092'] == 1].groupby(df['P3271']).sum()
        fr6 = (df['P7480S9e'][df['P3098'] == 1].groupby(df['P3271']).sum() +
              df['P7480S10e'][df['P3099'] == 1].groupby(df['P3271']).sum())


        # Fill the NoRen_1 DataFrame with the new column values.
        NoRen_1.loc['A'] = 'A', fr1[1], fr1[2], fr4[1], fr4[2]
        NoRen_1.loc['C'] = 'C', fr2[1], fr2[2], fr5[1], fr5[2]
        NoRen_1.loc['F'] = 'F', fr3[1], fr3[2], fr6[1], fr6[2]

        # Calculate the PuestosH, PuestosM, PrHourH, PrHourM, CoefH, and CoefM columns.
        NoRen_1['PuestosH'], NoRen_1['PuestosM'] = NoRen_1['HourH'] / 48, NoRen_1['HourM'] / 48
        NoRen_1['PrHourH'], NoRen_1['PrHourM'] = NoRen_1['HourH'] / NoRen_1['PerH'], NoRen_1['HourM'] / NoRen_1['PerM']
        NoRen_1['CoefH'], NoRen_1['CoefM'] = NoRen_1['PrHourH'] / 48, NoRen_1['PrHourM'] / 48

        # Calculate the PrMMH and PrMMfM columns.
        NoRen_1['PrMMH'], NoRen_1['PrMMfM'] = NoRen_1['HourH'] * 52 / 1000000, NoRen_1['HourM'] * 52 / 1000000

        return NoRen_1