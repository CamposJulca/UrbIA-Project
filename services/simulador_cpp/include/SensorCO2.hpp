#pragma once
#include "SensorBase.hpp"

class SensorCO2 : public SensorBase {
public:
    SensorCO2();
    std::string getTipo() const override;
    double leerValor() const override;
};
