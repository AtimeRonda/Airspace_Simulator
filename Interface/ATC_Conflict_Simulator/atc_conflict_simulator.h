#ifndef ATC_CONFLICT_SIMULATOR_H
#define ATC_CONFLICT_SIMULATOR_H

#include <QDialog>

namespace Ui {
class ATC_Conflict_Simulator;
}

class ATC_Conflict_Simulator : public QDialog
{
    Q_OBJECT

public:
    explicit ATC_Conflict_Simulator(QWidget *parent = 0);
    ~ATC_Conflict_Simulator();

private:
    Ui::ATC_Conflict_Simulator *ui;
};

#endif // ATC_CONFLICT_SIMULATOR_H
