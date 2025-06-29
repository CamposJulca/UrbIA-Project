#include "SensorCO2.hpp"
#include <cstdlib>

SensorCO2::SensorCO2() : SensorBase("CO2") {}

std::string SensorCO2::getTipo() const {
    return "co2";
}

double SensorCO2::leerValor() const {
    return 400.0 + static_cast<double>(std::rand() % 201);  // 400 - 600 ppm
}
