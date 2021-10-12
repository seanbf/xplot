from base64 import b64encode
import io
import streamlit as st
from datetime import datetime
import os

def export_name(name, datetime, original_file_name):
    
    if name == '':
        output_name = os.path.splitext(original_file_name)[0]
    else:
        output_name = name
    
    if datetime == True:
        export_datetime = "_" + str("{:%Y_%m_%d_%H_%M_%S}".format(datetime.now()))
    else:
        export_datetime = ''

    file_name = str(output_name) + str(export_datetime)

    return file_name

def show_export_format(col_export_format):         
    output_format = col_export_format.selectbox(label='Select download format', options=['.html', '.jpeg','.png', '.pdf', '.svg','.json'])
    return output_format

def download_chart(plot, quick_analysis_result, include_plotted_data, include_raw_data, plotted_data, raw_data, output_format, file_name, col_export_link):
    with st.spinner("Generating File to Export.."):
        """
        Convert chart to file to be exported and provide download link.
        """

        file_name_with_extension = file_name + output_format

        if output_format == '.html':
            buffer = io.StringIO()
            plot.write_html(buffer)
            quick_analysis_result.to_html(buffer)
            if include_plotted_data == True:
                plotted_data.to_html(buffer)
            if include_raw_data == True:
                raw_data.to_html(buffer)
            html_bytes = buffer.getvalue().encode()
            encoding = b64encode(html_bytes).decode()

            href = f'<a download={file_name_with_extension} href="data:file/html;base64,{encoding}" >{file_name_with_extension}</a>'

        if output_format == '.json':
            img_bytes = plot.to_image(format='json')
            encoding = b64encode(img_bytes).decode()

            href = f'<a download={file_name_with_extension} href="data:file/json;base64,{encoding}" >{file_name_with_extension}</a>'

        if output_format == '.png':
            img_bytes = plot.to_image(format='png')
            encoding = b64encode(img_bytes).decode()

            href = f'<a download={file_name_with_extension} href="data:image/png;base64,{encoding}" >{file_name_with_extension}</a>'

        if output_format == '.jpeg':
           img_bytes = plot.to_image(format='jpg')
           encoding = b64encode(img_bytes).decode()

           href = f'<a download={file_name_with_extension} href="data:image/jpeg;base64,{encoding}" >{file_name_with_extension}</a>'

        if output_format == '.svg':
           img_bytes = plot.to_image(format='svg')
           encoding = b64encode(img_bytes).decode()

           href = f'<a download={file_name_with_extension} href="data:image/svg;base64,{encoding}" >{file_name_with_extension}</a>'

        if output_format == '.pdf':
           img_bytes = plot.to_image(format='pdf')
           encoding = b64encode(img_bytes).decode()

           href = f'<a download={file_name_with_extension} href="data:file/pdf;base64,{encoding}" >{file_name_with_extension}</a>'

        return col_export_link.markdown(href, unsafe_allow_html=True)