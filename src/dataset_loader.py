import pandas as pd
from sklearn.model_selection import train_test_split

class DatasetLoader:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.required_columns = ['texto_completo', 'categoria']

    def load(self):
        # Read the CSV file as a single column, assuming each row is fully quoted.
        # header=None prevents the first row from being treated as headers initially.
        # names=['single_column_data'] gives a temporary name to this single column.
        df_raw = pd.read_csv(self.dataset_path, header=None, names=['single_column_data'])

        if df_raw.empty:
            raise ValueError("El dataset está vacío.")

        # The first row contains the actual header, e.g., '"texto_completo,categoria"'
        header_line = str(df_raw.iloc[0, 0]) # Ensure it's a string
        
        # Remove surrounding quotes from the header line and split to get actual column names
        expected_columns = [col.strip() for col in header_line.strip('"').split(',')]

        if len(expected_columns) != 2 or expected_columns[0] != 'texto_completo' or expected_columns[1] != 'categoria':
            # Fixed: Escaped the inner double quotes to resolve the SyntaxError
            raise ValueError(f"Formato de encabezado inesperado en el CSV. Se esperaba '\"texto_completo,categoria\"', se encontró '{header_line}'.")

        # Process data rows (from the second row onwards)
        df_data = df_raw.iloc[1:].copy()
        
        # Remove surrounding quotes from each data string
        df_data['single_column_data'] = df_data['single_column_data'].astype(str).str.strip('"')

        # Split the single column into two, splitting only on the *last* comma.
        # This assumes 'categoria' is always the part after the last comma.
        split_df = df_data['single_column_data'].str.rsplit(',', n=1, expand=True)

        if split_df.shape[1] < 2:
            raise ValueError("No se pudo dividir la columna de datos en 'texto_completo' y 'categoria'. Verifique el formato del CSV.")
        
        # Assign the correct column names
        split_df.columns = expected_columns
        
        # Reset index for the final DataFrame
        df_final = split_df.reset_index(drop=True)
        
        self._validate_columns(df_final)
        return df_final

    def prepare(self):
        df = self.load()
        # Assuming 'texto_completo' is the feature and 'categoria' is the target
        X = df['texto_completo']
        y = df['categoria']
        return X, y

    def split_data(self, X, y, test_size=0.2, random_state=42):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        return X_train, X_test, y_train, y_test

    def _validate_columns(self, df):
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Faltan columnas requeridas en el dataset: {missing_columns}")
