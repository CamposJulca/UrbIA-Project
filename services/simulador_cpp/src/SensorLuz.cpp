#include "SensorLuz.hpp"
#include <random>

SensorLuz::SensorLuz() : SensorBase("Luz") {}

std::string SensorLuz::getTipo() const {
    return "luz";
}

double SensorLuz::leerValor() const {
    static std::default_random_engine generator(std::random_device{}());
    std::uniform_real_distribution<double> distribution(0.0, 1000.0);
    return distribution(generator);  // Lux
}
