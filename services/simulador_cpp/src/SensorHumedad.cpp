#include "SensorHumedad.hpp"
#include <cstdlib>

SensorHumedad::SensorHumedad() : SensorBase("Humedad") {}

std::string SensorHumedad::getTipo() const {
    return "humedad";
}

double SensorHumedad::leerValor() const {
    return 40.0 + static_cast<double>(std::rand() % 4001) / 100.0;  // 40.0 - 80.0 %
}
