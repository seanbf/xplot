from base64 import b64encode
import io
import streamlit as st


@st.cache
def download_chart(plot, output_format):
    """

    :param plot: plotly figure
    :param output_format: str, the required output format in string
    :return:
    """

    file_name_with_extension = 'image1' + output_format

    if output_format == '.html':
        buffer = io.StringIO()
        plot.write_html(buffer)
        html_bytes = buffer.getvalue().encode()
        encoding = b64encode(html_bytes).decode()

        href = f'<a download={file_name_with_extension} href="data:file/html;base64,{encoding}" >Download</a>'

    if output_format == '.json':
        img_bytes = plot.to_image(format='json')
        encoding = b64encode(img_bytes).decode()

        href = f'<a download={file_name_with_extension} href="data:file/json;base64,{encoding}" >Download</a>'

    if output_format == '.png':
        img_bytes = plot.to_image(format='png')
        encoding = b64encode(img_bytes).decode()

        href = f'<a download={file_name_with_extension} href="data:image/png;base64,{encoding}" >Download</a>'

    if output_format == '.jpeg':
        img_bytes = plot.to_image(format='jpg')
        encoding = b64encode(img_bytes).decode()

        href = f'<a download={file_name_with_extension} href="data:image/jpeg;base64,{encoding}" >Download</a>'

    if output_format == '.svg':
        img_bytes = plot.to_image(format='svg')
        encoding = b64encode(img_bytes).decode()

        href = f'<a download={file_name_with_extension} href="data:image/svg;base64,{encoding}" >Download</a>'

    if output_format == '.pdf':
        img_bytes = plot.to_image(format='pdf')
        encoding = b64encode(img_bytes).decode()

        href = f'<a download={file_name_with_extension} href="data:file/pdf;base64,{encoding}" >Download</a>'

    return href


def show_export_format(plot):
    try:
        st.subheader('Export image')
        output_format = st.selectbox(label='Select download format', options=['.png', '.jpeg', '.pdf', '.svg',
                                                                              '.html', '.json'])
        href = download_chart(plot, output_format=output_format)
        st.markdown(href, unsafe_allow_html=True)
    except Exception as e:
        print(e)
