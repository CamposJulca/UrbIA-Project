package urbia.model;

public class SensorLectura {
    private long timestamp;
    private String clave;
    private String valor;

    public SensorLectura(long timestamp, String clave, String valor) {
        this.timestamp = timestamp;
        this.clave = clave;
        this.valor = valor;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public String getClave() {
        return clave;
    }

    public String getValor() {
        return valor;
    }
}
