/********************************************************************************
** Form generated from reading UI file 'atc_conflict_simulator.ui'
**
** Created by: Qt User Interface Compiler version 5.9.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_ATC_CONFLICT_SIMULATOR_H
#define UI_ATC_CONFLICT_SIMULATOR_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QDialog>
#include <QtWidgets/QHeaderView>

QT_BEGIN_NAMESPACE

class Ui_ATC_Conflict_Simulator
{
public:

    void setupUi(QDialog *ATC_Conflict_Simulator)
    {
        if (ATC_Conflict_Simulator->objectName().isEmpty())
            ATC_Conflict_Simulator->setObjectName(QStringLiteral("ATC_Conflict_Simulator"));
        ATC_Conflict_Simulator->resize(1300, 700);
        QSizePolicy sizePolicy(QSizePolicy::Maximum, QSizePolicy::Maximum);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(ATC_Conflict_Simulator->sizePolicy().hasHeightForWidth());
        ATC_Conflict_Simulator->setSizePolicy(sizePolicy);

        retranslateUi(ATC_Conflict_Simulator);

        QMetaObject::connectSlotsByName(ATC_Conflict_Simulator);
    } // setupUi

    void retranslateUi(QDialog *ATC_Conflict_Simulator)
    {
        ATC_Conflict_Simulator->setWindowTitle(QApplication::translate("ATC_Conflict_Simulator", "ATC_Conflict_Simulator", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class ATC_Conflict_Simulator: public Ui_ATC_Conflict_Simulator {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ATC_CONFLICT_SIMULATOR_H
