package urbia.utils;

import urbia.models.SensorReading;

import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.List;

public class CsvExporter {

    public static void exportar(List<SensorReading> datos, String nombreDispositivo) {
        String filename = "lecturas_" + nombreDispositivo.replaceAll("\\s+", "_").toLowerCase() + ".csv";

        try (PrintWriter writer = new PrintWriter(new FileWriter(filename))) {
            writer.println("timestamp,variable,valor");

            for (SensorReading lectura : datos) {
                writer.printf("%s,%s,%s%n",
                        lectura.getFormattedTimestamp(),
                        lectura.getVariable(),
                        lectura.getValue());
            }

            System.out.printf("📁 Archivo CSV generado exitosamente: %s%n", filename);

        } catch (Exception e) {
            System.out.println("❌ Error al exportar a CSV: " + e.getMessage());
        }
    }
}
