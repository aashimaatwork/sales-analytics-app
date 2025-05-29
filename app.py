import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    secondary = pd.read_csv('data/secondary_sales.csv')
    projections = pd.read_csv('data/projections.csv')
    targets = pd.read_csv('data/key_account_targets.csv')
    products = pd.read_csv('data/product_master.csv')
    return secondary, projections, targets, products

def pareto_accounts(df, product_id):
    # Filter for product
    prod_df = df[df['product_id'] == product_id]
    # Aggregate sales by account
    sales_by_account = prod_df.groupby('account_id')['sales_value'].sum().sort_values(ascending=False)
    # Calculate cumulative percentage
    cumsum = sales_by_account.cumsum()
    total = sales_by_account.sum()
    pareto = sales_by_account[cumsum <= 0.8 * total]
    return pareto

def main():
    st.title("Sales Pipeline Dashboard")
    secondary, projections, targets, products = load_data()
    selected_product = st.selectbox("Select Product", products['product_id'].unique())
    
    # 80/20 accounts for this product
    pareto = pareto_accounts(secondary, selected_product)
    st.write(f"Accounts contributing 80% of sales for {selected_product}:")
    st.dataframe(pareto)
    
    # Key accounts for this product
    key_accounts = targets[targets['product_id'] == selected_product]['account_id'].unique()
    st.write(f"Key accounts for {selected_product}:")
    st.write(key_accounts)

if __name__ == "__main__":
    main()
