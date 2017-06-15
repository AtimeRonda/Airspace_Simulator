#include "atc_conflict_simulator.h"
#include "ui_atc_conflict_simulator.h"

ATC_Conflict_Simulator::ATC_Conflict_Simulator(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::ATC_Conflict_Simulator)
{
    ui->setupUi(this);
}

ATC_Conflict_Simulator::~ATC_Conflict_Simulator()
{
    delete ui;
}
