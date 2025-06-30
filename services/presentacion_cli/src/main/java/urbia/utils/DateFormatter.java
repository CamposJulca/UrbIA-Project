package urbia.utils;

import java.time.Instant;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;

public class DateFormatter {

    private static final DateTimeFormatter FORMATTER = DateTimeFormatter
            .ofPattern("yyyy-MM-dd HH:mm:ss")
            .withZone(ZoneId.systemDefault());

    public static String formatear(long timestamp) {
        try {
            Instant instant = Instant.ofEpochMilli(timestamp);
            return FORMATTER.format(instant);
        } catch (Exception e) {
            return "fecha inválida";
        }
    }
}
