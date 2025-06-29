#include "SensorPresion.hpp"
#include <random>

SensorPresion::SensorPresion() : SensorBase("Presion") {}

std::string SensorPresion::getTipo() const {
    return "presion";
}

double SensorPresion::leerValor() const {
    static std::default_random_engine generator(std::random_device{}());
    std::uniform_real_distribution<double> distribution(990.0, 1025.0);
    return distribution(generator);  // hPa
}
