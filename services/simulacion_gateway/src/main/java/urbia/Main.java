package urbia;

import urbia.api.ThingsBoardClient;
import urbia.models.SensorLectura;


import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        System.out.println("\n🌐 UrbIA :: Cliente Java para ThingsBoard\n");

        ThingsBoardClient cliente = new ThingsBoardClient();
        System.out.println("🧑 Usuario ThingsBoard: autenticando...");
        if (!cliente.autenticar()) {
            System.out.println("❌ No se pudo autenticar. Verifique sus credenciales.");
            return;
        }

        Scanner sc = new Scanner(System.in);

        while (true) {
            List<Map<String, String>> dispositivos = cliente.obtenerDispositivos();
            if (dispositivos.isEmpty()) {
                System.out.println("⚠️ No se encontraron dispositivos.");
                return;
            }

            System.out.println("\n📋 Menú de opciones:");
            for (int i = 0; i < dispositivos.size(); i++) {
                String nombre = dispositivos.get(i).get("name");
                System.out.printf("%d) %s%s\n", i + 1, nombre, (i == 0 ? " [default]" : ""));
            }
            System.out.println("0) Salir\n");
            System.out.print("👉 Seleccione un dispositivo: ");
            int opcion = sc.nextInt();

            if (opcion == 0) break;

            if (opcion < 1 || opcion > dispositivos.size()) {
                System.out.println("❌ Opción inválida.");
                continue;
            }

            Map<String, String> dispositivo = dispositivos.get(opcion - 1);
            String deviceId = dispositivo.get("id");
            String nombreDispositivo = dispositivo.get("name");

            List<SensorLectura> lecturas = cliente.obtenerLecturas(deviceId);
            System.out.println("\n📈 Últimas lecturas de: " + nombreDispositivo);
            for (SensorLectura lectura : lecturas) {
                Date fecha = new Date(lectura.getTimestamp());
                System.out.printf("📌 [%s] %s = %s\n", fecha.toString(), lectura.getClave(), lectura.getValor());
            }

            System.out.print("\n💾 ¿Desea exportar estas lecturas? (s/n): ");
            String exportar = sc.next();
            if (exportar.equalsIgnoreCase("s")) {
                exportarCSV(lecturas, nombreDispositivo);
            }
        }

        System.out.println("👋 Programa finalizado.");
    }

    private static void exportarCSV(List<SensorLectura> datos, String nombreDispositivo) {
        String filename = "lecturas_" + nombreDispositivo + ".csv";
        try (PrintWriter writer = new PrintWriter(new FileWriter(filename))) {
            writer.println("timestamp,variable,valor");
            for (SensorLectura lectura : datos) {
                Date fecha = new Date(lectura.getTimestamp());
                writer.printf("%s,%s,%s%n", fecha.toString(), lectura.getClave(), lectura.getValor());
            }
            System.out.println("📁 Archivo CSV generado: " + filename);
        } catch (Exception e) {
            System.out.println("❌ Error al escribir el archivo CSV: " + e.getMessage());
        }
    }
}
