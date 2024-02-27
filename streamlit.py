import streamlit as st
import pandas as pd
import requests

# Define the function to handle the button click
def fetch_data(orderid, naverid):
    # Define the API endpoint
    url = 'https://script.google.com/macros/s/AKfycbzLaZvxl_PjyJKLgAPkCxHjh-Yj1M_9jqyj9RcYeR4mnr7W7By0T8ZsTm7XWilaispW1Q/exec'
    
    # Set the parameters for the GET request
    params = {'naverid': naverid, 'orderid': orderid}
    
    # Make the GET request
    response = requests.get(url, params=params)
    
    # Check if the response was successful
    if response.status_code == 200:
        try:
            # Parse the JSON response
            data = response.json()

            # If the API returns a list directly, we can create the DataFrame from it
            if isinstance(data, list):
                df = pd.DataFrame(data)
            # If the API returns a dictionary, check for a specific key (e.g., 'data') that contains the list
            elif 'data' in data:
                df = pd.DataFrame(data['data'])
            else:
                print("Unexpected JSON structure:", data)
                return None
            
            # Optionally, rename columns to match desired DataFrame structure
            df.rename(columns={
                'ProductOrderNum': '네이버주문번호',
                'Code': '코드',
                'Productname': '상품이름',
                'Sent_to': '송신한 네이버 아이디',
                'sent_date': '발송일'
            }, inplace=True)
            
            return df
        except ValueError as e:
            print("Error processing JSON response:", e)
    else:
        print(f"Failed to fetch data, HTTP status code: {response.status_code}")

st.title('키를 찾으세요')
st.header('발송된 키를 이력을 확인할 수 있습니다.')
st.subheader('네이버아이디와 주문번호를 입력해보세요. 관련 정보가 나옵니다.')

# Text Input
naverid = st.text_input("주문하신 네이버아이디를 입력하세요", "예시:aaaa")
# Text Input
orderid = st.text_input("주문번호를 입력하세요. 숫자만 입력하세요.", "예시:1234")

if st.button("검색"):    
    st.write("네이버아이디: " + naverid + " 주문번호: " + orderid + " 에 대한 배송여부확인결과입니다.")    
    #naverid = naverid.title()
    #orderid = orderid.title()
    df = fetch_data(orderid,naverid)
    try:
        if len(df) == 0:
            st.write('검색된 배송 데이터가 없습니다. 문의 바랍니다.')
        else:
            # CSS to inject contained in a string
            hide_table_row_index = """
                        <style>
                        thead tr th:first-child {display:none}
                        tbody th {display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            
            # Display a static table
            st.table(df)
    except:
        st.write("에러가 발생했습니다.")
