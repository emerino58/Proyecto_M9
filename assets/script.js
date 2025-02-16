document.addEventListener("DOMContentLoaded", function() {
    console.log("Script de PDF e impresión cargado correctamente.");

    function setupPDFButton(buttonId, contentId, filename) {
        let button = document.getElementById(buttonId);
        if (button) {
            button.addEventListener("click", function() {
                console.log(`Generando PDF: ${filename}`);
                let element = document.getElementById(contentId);
                
                if (!element) {
                    console.error(`Error: No se encontró el elemento '${contentId}'.`);
                    alert(`Error: No se encontró el contenido a exportar.`);
                    return;
                }

                let opt = {
                    margin: 10,
                    filename: filename,
                    image: { type: 'jpeg', quality: 0.98 },
                    html2canvas: { scale: 2 },
                    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
                };

                html2pdf().from(element).set(opt).save();
            });
        }
    }

    function setupPrintButton(buttonId) {
        let button = document.getElementById(buttonId);
        if (button) {
            button.addEventListener("click", function() {
                window.print();
            });
        }
    }

    // 📌 Configurar los botones de PDF e impresión en los tres módulos

    // 📊 Módulo de Estadísticas
    setupPDFButton("btn-pdf-estadisticas", "content-to-export-estadisticas", "estadisticas_jugadores.pdf");
    setupPrintButton("btn-print-estadisticas");

    // 📊 Módulo de Tabla de Posiciones
    setupPDFButton("btn-pdf-posiciones", "content-to-export-posiciones", "tabla_posiciones.pdf");
    setupPrintButton("btn-print-posiciones");

    // 📊 Módulo de Antropometría
    setupPDFButton("btn-pdf-antropometria", "content-to-export-antropometria", "datos_antropometricos.pdf");
    setupPrintButton("btn-print-antropometria");
});
