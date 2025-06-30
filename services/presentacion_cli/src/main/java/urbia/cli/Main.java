package urbia.cli;

import urbia.services.AuthService;
import urbia.services.DeviceService;
import urbia.services.TelemetryService;
import urbia.utils.CsvExporter;
import urbia.models.DeviceInfo;
import urbia.models.SensorReading;

import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        System.out.println("🌐 UrbIA CLI :: Cliente de consola para ThingsBoard\n");

        AuthService authService = new AuthService();
        String token = authService.autenticar();

        if (token == null || token.isEmpty()) {
            System.out.println("❌ No se pudo autenticar con ThingsBoard. Verifica el archivo .env");
            return;
        }

        DeviceService deviceService = new DeviceService(token);
        List<DeviceInfo> dispositivos = deviceService.obtenerDispositivos();

        if (dispositivos.isEmpty()) {
            System.out.println("⚠️ No se encontraron dispositivos disponibles.");
            return;
        }

        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.println("\n📋 Dispositivos disponibles:");
            for (int i = 0; i < dispositivos.size(); i++) {
                System.out.printf("%d) %s%n", i + 1, dispositivos.get(i).getName());
            }
            System.out.println("0) Salir");
            System.out.print("👉 Seleccione un dispositivo: ");

            int opcion;
            try {
                opcion = Integer.parseInt(scanner.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("❌ Entrada inválida. Intente de nuevo.");
                continue;
            }

            if (opcion == 0) break;
            if (opcion < 1 || opcion > dispositivos.size()) {
                System.out.println("❌ Opción fuera de rango.");
                continue;
            }

            DeviceInfo seleccionado = dispositivos.get(opcion - 1);
            System.out.printf("📌 Dispositivo seleccionado: %s%n", seleccionado.getName());

            TelemetryService telemetryService = new TelemetryService(token);
            List<SensorReading> lecturas = telemetryService.obtenerLecturasRecientes(seleccionado.getId());

            if (lecturas.isEmpty()) {
                System.out.println("⚠️ No hay lecturas disponibles para este dispositivo.");
            } else {
                System.out.println("📈 Últimas lecturas:");
                for (SensorReading lectura : lecturas) {
                    System.out.printf("📍 [%s] %s = %s%n",
                            lectura.getFormattedTimestamp(),
                            lectura.getVariable(),
                            lectura.getValue());
                }

                System.out.print("💾 ¿Desea exportar a CSV? (s/n): ");
                String respuesta = scanner.nextLine().trim().toLowerCase();
                if (respuesta.equals("s")) {
                    CsvExporter.exportar(lecturas, seleccionado.getName());
                }
            }
        }

        System.out.println("👋 Gracias por usar UrbIA CLI. Hasta pronto.");
    }
}
    