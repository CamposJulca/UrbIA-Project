#pragma once
#include "SensorBase.hpp"

class SensorLuz : public SensorBase {
public:
    SensorLuz();
    std::string getTipo() const override;
    double leerValor() const override;
};
