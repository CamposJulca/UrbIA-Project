#pragma once
#include "SensorBase.hpp"

class SensorHumedad : public SensorBase {
public:
    SensorHumedad();
    std::string getTipo() const override;
    double leerValor() const override;
};
