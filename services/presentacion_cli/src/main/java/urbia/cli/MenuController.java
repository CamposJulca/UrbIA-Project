package urbia.cli;

import urbia.models.DeviceInfo;
import urbia.models.SensorReading;
import urbia.services.DeviceService;
import urbia.services.TelemetryService;
import urbia.utils.CsvExporter;

import java.util.List;
import java.util.Scanner;

public class MenuController {

    private final Scanner scanner;
    private final String token;

    public MenuController(String token) {
        this.token = token;
        this.scanner = new Scanner(System.in);
    }

    public void iniciar() {
        mostrarBienvenida();

        DeviceService deviceService = new DeviceService(token);
        List<DeviceInfo> dispositivos = deviceService.obtenerDispositivos();

        if (dispositivos.isEmpty()) {
            System.out.println("⚠️  No se encontraron dispositivos disponibles en ThingsBoard.");
            return;
        }

        while (true) {
            mostrarMenuDispositivos(dispositivos);
            int opcion = leerOpcion(dispositivos.size());

            if (opcion == 0) {
                if (confirmarSalida()) break;
                else continue;
            }

            DeviceInfo seleccionado = dispositivos.get(opcion - 1);
            manejarDispositivo(seleccionado);
        }

        System.out.println("✅ Sesión finalizada correctamente.");
    }

    private void mostrarBienvenida() {
        System.out.println("""
                ┌──────────────────────────────────────────────┐
                │ 🌐 UrbIA CLI - Cliente de monitoreo IoT       │
                └──────────────────────────────────────────────┘
                Bienvenido. Este sistema permite:
                - Consultar dispositivos registrados
                - Visualizar lecturas recientes de sensores
                - Exportar las lecturas a un archivo CSV

                ℹ️ Use los números del menú para navegar.
                ❓ En cualquier momento, escriba "?" para ayuda.
                """);
    }

    private void mostrarMenuDispositivos(List<DeviceInfo> dispositivos) {
        System.out.println("\n📋 Lista de dispositivos disponibles:");
        for (int i = 0; i < dispositivos.size(); i++) {
            System.out.printf(" %2d) %s%n", i + 1, dispositivos.get(i).getName());
        }
        System.out.println("  0) Salir");
        System.out.print("👉 Seleccione un dispositivo: ");
    }

    private int leerOpcion(int max) {
        String entrada = scanner.nextLine().trim();

        if (entrada.equals("?")) {
            System.out.println("""
                ℹ️ AYUDA:
                - Ingrese un número entre 1 y %d para seleccionar un dispositivo.
                - Ingrese 0 para salir del sistema.
                - Después de visualizar lecturas, podrá exportarlas a CSV.
                """.formatted(max));
            return leerOpcion(max);
        }

        try {
            int opcion = Integer.parseInt(entrada);
            if (opcion >= 0 && opcion <= max) {
                return opcion;
            }
        } catch (NumberFormatException ignored) {}

        System.out.println("❌ Entrada inválida. Intente de nuevo.");
        return leerOpcion(max);
    }

    private void manejarDispositivo(DeviceInfo dispositivo) {
        System.out.printf("%n📌 Dispositivo seleccionado: %s%n", dispositivo.getName());

        TelemetryService telemetryService = new TelemetryService(token);
        List<SensorReading> lecturas = telemetryService.obtenerLecturasRecientes(dispositivo.getId());

        if (lecturas.isEmpty()) {
            System.out.println("⚠️  No se encontraron lecturas recientes para este dispositivo.");
            return;
        }

        System.out.println("📈 Últimas lecturas disponibles:");
        for (SensorReading lectura : lecturas) {
            System.out.printf("📍 [%s] %s = %s%n",
                    lectura.getFormattedTimestamp(),
                    lectura.getVariable(),
                    lectura.getValue());
        }

        System.out.print("\n💾 ¿Desea exportar estas lecturas a CSV? (s/n): ");
        String respuesta = scanner.nextLine().trim().toLowerCase();
        if (respuesta.equals("s")) {
            CsvExporter.exportar(lecturas, dispositivo.getName());
        } else {
            System.out.println("📁 Exportación omitida.");
        }
    }

    private boolean confirmarSalida() {
        System.out.print("❓ ¿Está seguro de que desea salir? (s/n): ");
        String respuesta = scanner.nextLine().trim().toLowerCase();
        return respuesta.equals("s") || respuesta.equals("si");
    }
}
