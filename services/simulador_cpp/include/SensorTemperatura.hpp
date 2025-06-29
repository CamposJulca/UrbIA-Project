#pragma once
#include "SensorBase.hpp"

class SensorTemperatura : public SensorBase {
public:
    SensorTemperatura();
    std::string getTipo() const override;
    double leerValor() const override;
};
