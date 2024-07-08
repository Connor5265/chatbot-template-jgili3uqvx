from azure.storage.blob import BlobServiceClient
import config

# def read_dataset_from_adls(adls_parquet_file, container_input, directory):
    
#     # Print
#     print('Reading from Adls:', adls_parquet_file)
    
#     # Set up Azure Blob Connectivity
#     blob_service = BlobServiceClient.from_connection_string(config.CONNECTION_STRING)
#     container_client = blob_service.get_container_client(container_input + '/' + directory)

#     # Required Columns Sales Order
#     sales_order_columns = [
#                             'CREATEDON',
#                             '/BIC/ZZDOC_NUM',
#                             '/BIC/ZS_ORD_IT',
#                             '/BIC/ZLPRODNUM',
#                             '/BIC/ZLCUSNUM2',
#                             'ORDER_QTY',
#                             'NET_VALUE',
#                             '/BIC/ZLSREPNUM',
#                             '/BIC/ZLAREGNUM',
#                             '/BIC/ZLPTERTRY'
#                         ]
    
#     # Territory Master
#     terr_mstr = [
#                         '/BIC/ZPOSITION',
#                         '/BIC/ZPARTYID',
#                         '/BIC/ZRGNMGRID',
#                         '/BIC/ZMGRPOSNM',
#                         '/BIC/ZMDDPHL3',
#                         '/BIC/ZSPMCTERD',
#                         'ZPARTC_NAME',
#                         'EMAIL_ADDR',
#                     ]
    
#     # Legacy Territory XREF
#     legacy_terr_xref = [
#                         '/BIC/ZLCOMPNUM',
#                         '/BIC/ZLSREPNUM',
#                         '/BIC/ZSREPNUM'
#                     ]
    
#     # Legacy Customer Master
#     leg_cust_mstr_columns = ['Cust_Num','Cust_Name','Customer_Type','Street','Postcd_GIS','City','Country','Region','County','State', 'Phone', 'Phone_Type']
    
#     # Required_column Set
#     reqd_cols = {
#                     'salesordersb1t'        : sales_order_columns,
#                     'salesrepcrossref1bt'   : legacy_terr_xref,
#                     'salesrepmaster1bt'     : terr_mstr,
#                     'legacycustomermaster'  : leg_cust_mstr_columns,
#                  }
    
#     # Read the dataset into stream
#     stream = BytesIO()
#     container_client.download_blob(adls_parquet_file).readinto(stream)
#     stream.seek(0)
#     #
#     initial_dataframe = pd.read_parquet(stream, columns=reqd_cols[directory])
#     #
    
#     print('Reading Complete. Shape:', initial_dataframe.shape)
    
#     return initial_dataframe

def write_data_to_azure_blob(container_output, directory, filename, data_set):
    
    """
    Export data into Azure Blob
    """
    # Set up Azure Blob Connectivity
    blob_service        = BlobServiceClient.from_connection_string(config.CONNECTION_STRING) 
    container_client    = blob_service.get_container_client(container_output + '/' + directory)
    
    # Instantiate a new BlobClient
    blob_client     = container_client.get_blob_client(filename)
        
    # Upload data
    output = data_set.to_csv (index=False, encoding = "utf-8")
    try:
        blob_client.upload_blob(output, blob_type="BlockBlob", overwrite=True)
        print('File Uploaded Sucessfully!', filename)
    except Exception as e:
        print('File Upload Failed!', e)
    
    return