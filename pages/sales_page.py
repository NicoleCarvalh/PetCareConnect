from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QMessageBox
from PyQt5.QtGui import *
from backend.routes import format_date, format_value
from backend.endpoints.sales import get_sales_list

def populate_sales_table(self):
  inter_font_path = 'resources/fonts/Inter/Inter.ttf'
  montserrat_font_path = 'resources/fonts/Montserrat/static/Montserrat-Medium.ttf'
  QFontDatabase.addApplicationFont(inter_font_path)
  QFontDatabase.addApplicationFont(montserrat_font_path)

  inter_font_family = 'Inter'
  montserrat_font_family = 'MontserratM'

  header_font = QFont(inter_font_family, 11)
  header_font.setWeight(500)
  text_font = QFont(montserrat_font_family, 11)

  self.sales_table.horizontalHeader().setVisible(True)

  for i in range(6):
    self.sales_table.horizontalHeaderItem(i).setFont(header_font) 

  self.sales_table.setFont(text_font)

  def view_items(row):
    sale_id = int(self.sales_table.item(row, 0).text())

    sale = sales_data[row]

    items_details = []

    for item in sale['products']:
      product_id = item['product_id']

      product_name = item['product']['name']
      quantity = item['quantity']
      
      price = item['product']['sale_price']
      items_details.append(f"\n ID: {product_id} - {product_name} - {quantity} unidades - R${price:.2f}")

    items_text = "\n".join(items_details)
    
    items_dialog = QMessageBox()
    items_dialog.setWindowIcon(QIcon('resources/images/DesktopIcon.png'))
    items_dialog.setWindowTitle("Itens da Venda")
    items_dialog.setText(f"Itens da Venda ID {sale_id}:\n{items_text}")
    items_dialog.exec_()

  self.sales_table.setColumnWidth(0, 90)
  self.sales_table.setColumnWidth(1, 310)
  self.sales_table.setColumnWidth(2, 300)
  self.sales_table.setColumnWidth(3, 280)
  self.sales_table.setColumnWidth(4, 290)
  self.sales_table.setColumnWidth(5, 110)
  self.sales_table.setStyleSheet(
    "alternate-background-color: #F8E7BB;"
    "background-color: white;"
  )

  sales_data = get_sales_list()

  row_count = len(sales_data)

  self.sales_table.setRowCount(row_count)

  for row, sale in enumerate(sales_data):
    self.sales_table.setItem(row, 0, QTableWidgetItem(str(sale['id'])))
    self.sales_table.setItem(row, 1, QTableWidgetItem(str(sale['client']['name'])))
    self.sales_table.setItem(row, 2, QTableWidgetItem(format_date(sale['date_time'])))
    self.sales_table.setItem(row, 3, QTableWidgetItem(format_value(sale['total'])))
    self.sales_table.setItem(row, 4, QTableWidgetItem(str(sale['payment_method'])))

    btn_view_items = QPushButton("Ver Itens")
    btn_view_items.setFont(text_font)
    btn_view_items.clicked.connect(lambda _, row=row: view_items(row))
    self.sales_table.setCellWidget(row, 5, btn_view_items)
    btn_view_items.setStyleSheet(
      "background-color: #F8E7BB;"
    )
    self.sales_table.setRowHeight(row, 70)

