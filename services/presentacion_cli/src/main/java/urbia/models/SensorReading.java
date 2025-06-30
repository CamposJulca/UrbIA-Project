package urbia.models;

public class SensorReading {

    private final long timestamp;
    private final String variable;
    private final String value;
    private final String formattedTimestamp;

    public SensorReading(long timestamp, String variable, String value, String formattedTimestamp) {
        this.timestamp = timestamp;
        this.variable = variable;
        this.value = value;
        this.formattedTimestamp = formattedTimestamp;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public String getVariable() {
        return variable;
    }

    public String getValue() {
        return value;
    }

    public String getFormattedTimestamp() {
        return formattedTimestamp;
    }
}
