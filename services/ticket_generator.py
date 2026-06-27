from core.models import Compra, DetalleCompra

class TicketGenerator:
    """
    Clase encargada exclusivamente de formatear los datos de una Compra
    en diferentes representaciones (HTML, Texto, etc.).
    """
    
    @staticmethod
    def generar_html(compra: Compra) -> str:
        """Genera el HTML del ticket con formato profesional y espaciado"""
        
        total_fmt = f"$ {compra.total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        # Generar las filas de detalles
        detalles_html = ""
        for detalle in compra.detalles:
            precio_fmt = f"$ {detalle.precio_unitario:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            subtotal_fmt = f"$ {detalle.subtotal:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            
            detalles_html += f"""
            <tr>
                <td class="col-codigo"><b>{detalle.codigo_producto}</b></td>
                <td class="col-descripcion">{detalle.descripcion}</td>
                <td class="col-cantidad">{detalle.cantidad} x {precio_fmt}</td>
                <td class="col-subtotal"><b>{subtotal_fmt}</b></td>
            </tr>
            """
        
        # HTML completo del ticket
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    font-size: 11pt;
                    margin: 0;
                    padding: 20px;
                    color: #000;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 20px;
                    border-bottom: 2px solid #000;
                    padding-bottom: 10px;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 16pt;
                    letter-spacing: 1px;
                }}
                .header p {{
                    margin: 5px 0;
                    font-size: 10pt;
                }}
                .info {{
                    margin-bottom: 15px;
                    font-size: 10pt;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                .col-codigo {{ width: 20%; padding-right: 15px; vertical-align: top; }}
                .col-descripcion {{ width: 40%; padding-left: 5px; padding-right: 10px; vertical-align: top; }}
                .col-cantidad {{ width: 20%; text-align: right; padding-right: 15px; vertical-align: top; }}
                .col-subtotal {{ width: 20%; text-align: right; vertical-align: top; }}
                tr {{ border-bottom: 1px dashed #ccc; }}
                .total {{
                    border-top: 2px solid #000;
                    padding-top: 10px;
                    text-align: right;
                    font-size: 13pt;
                    margin-top: 10px;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    border-top: 1px solid #ccc;
                    padding-top: 10px;
                    font-size: 9pt;
                    color: #555;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>BANDERÍN - LIBRERÍA</h1>
                <p><b>TICKET DE COMPRA A PROVEEDOR</b></p>
            </div>
            
            <div class="info">
                <p><b>N° Compra:</b> {compra.id}</p>
                <p><b>Fecha:</b> {compra.get_fecha_formateada()}</p>
            </div>
            
            <table>
                <thead>
                    <tr style="border-bottom: 2px solid #000;">
                        <th class="col-codigo" style="text-align: left;">Código</th>
                        <th class="col-descripcion" style="text-align: left;">Descripción</th>
                        <th class="col-cantidad" style="text-align: right;">Detalle</th>
                        <th class="col-subtotal" style="text-align: right;">Subtotal</th>
                    </tr>
                </thead>
                <tbody>
                    {detalles_html}
                </tbody>
            </table>
            
            <div class="total">
                <p><b>TOTAL: {total_fmt}</b></p>
                <p style="font-size: 10pt; font-weight: normal;">Items: {compra.cantidad_items}</p>
            </div>
            
            <div class="footer">
                <p>Registro interno de compras - Banderín</p>
            </div>
        </body>
        </html>
        """
        
        return html
