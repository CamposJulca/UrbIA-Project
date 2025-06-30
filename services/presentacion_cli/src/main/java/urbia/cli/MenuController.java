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
        DeviceService deviceService = new DeviceService(token);
        List<DeviceInfo> dispositivos = deviceService.obtenerDispositivos();

        if (dispositivos.isEmpty()) {
            System.out.println("⚠️ No se encontraron dispositivos.");
            return;
        }

        while (true) {
            mostrarMenuDispositivos(dispositivos);
            int opcion = leerOpcion(dispositivos.size());

            if (opcion == 0) {
                System.out.println("👋 Saliendo del sistema...");
                break;
            }

            DeviceInfo seleccionado = dispositivos.get(opcion - 1);
            manejarDispositivo(seleccionado);
        }
    }

    private void mostrarMenuDispositivos(List<DeviceInfo> dispositivos) {
        System.out.println("\n📋 Dispositivos disponibles:");
        for (int i = 0; i < dispositivos.size(); i++) {
            System.out.printf("%d) %s%n", i + 1, dispositivos.get(i).getName());
        }
        System.out.println("0) Salir");
        System.out.print("👉 Seleccione un dispositivo: ");
    }

    private int leerOpcion(int max) {
        try {
            int opcion = Integer.parseInt(scanner.nextLine());
            if (opcion >= 0 && opcion <= max) {
                return opcion;
            }
        } catch (NumberFormatException ignored) {}
        System.out.println("❌ Entrada inválida. Intente de nuevo.");
        return leerOpcion(max);
    }

    private void manejarDispositivo(DeviceInfo dispositivo) {
        System.out.printf("📌 Dispositivo seleccionado: %s%n", dispositivo.getName());

        TelemetryService telemetryService = new TelemetryService(token);
        List<SensorReading> lecturas = telemetryService.obtenerLecturasRecientes(dispositivo.getId());

        if (lecturas.isEmpty()) {
            System.out.println("⚠️ No hay lecturas disponibles para este dispositivo.");
            return;
        }

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
            CsvExporter.exportar(lecturas, dispositivo.getName());
        }
    }
}
