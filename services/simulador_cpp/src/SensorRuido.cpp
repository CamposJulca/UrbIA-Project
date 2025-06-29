#include "SensorRuido.hpp"
#include <random>

SensorRuido::SensorRuido() : SensorBase("Ruido") {}

std::string SensorRuido::getTipo() const {
    return "ruido";
}

double SensorRuido::leerValor() const {
    static std::default_random_engine generator(std::random_device{}());
    std::uniform_real_distribution<double> distribution(30.0, 120.0);
    return distribution(generator);  // dB
}
