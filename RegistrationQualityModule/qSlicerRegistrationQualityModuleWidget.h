#ifndef __qSlicerRegistrationQualityModuleWidget_h
#define __qSlicerRegistrationQualityModuleWidget_h

// SlicerQt includes
#include "qSlicerAbstractModuleWidget.h"

#include "qSlicerRegistrationQualityModuleExport.h"

#include <vtkMRMLVectorVolumeNode.h>
#include <vtkMRMLGridTransformNode.h>

class qSlicerRegistrationQualityModuleWidgetPrivate;
class vtkMRMLNode;
class QMenu;

/// \ingroup Slicer_QtModules_RegistrationQuality
class Q_SLICER_QTMODULES_REGISTRATIONQUALITY_EXPORT qSlicerRegistrationQualityModuleWidget :
	public qSlicerAbstractModuleWidget {

	Q_OBJECT
	QVTK_OBJECT

public:
	typedef qSlicerAbstractModuleWidget Superclass;
	qSlicerRegistrationQualityModuleWidget(QWidget *parent=0);
	virtual ~qSlicerRegistrationQualityModuleWidget();

	virtual void enter();
        virtual bool setEditedNode(vtkMRMLNode* node, QString role = QString(), QString context = QString());
        

public slots:
	virtual void setMRMLScene(vtkMRMLScene*);
	void onSceneImportedEvent();
	void setRegistrationQualityParametersNode(vtkMRMLNode *node);
	void updateWidgetFromMRML();
        

protected slots:
	void onLogicModified();
        void updateButtonsAndTable();

	// new

	void fixedVolumeChanged(vtkMRMLNode*);
        void movingVolumeChanged(vtkMRMLNode*);
        void forwardWarpedVolumeChanged(vtkMRMLNode*);
        void backwardWarpedVolumeChanged(vtkMRMLNode*);

        void vectorVolumeChanged(vtkMRMLNode*);
        void invVectorVolumeChanged(vtkMRMLNode*);
        
        void outputModelChanged(vtkMRMLNode*);
        void outputDirectoyChanged();
        void ROIChanged(vtkMRMLNode*);
        void fixedFiducialChanged(vtkMRMLNode*);
        void movingFiducialChanged(vtkMRMLNode*);
        
        void FixedSegmentIDChanged(QString);
        void MovingSegmentIDChanged(QString);
        void fixedSegmentationNodeChanged(vtkMRMLNode*);
        void movingSegmentationNodeChanged(vtkMRMLNode*);
        
        void movieBoxRedStateChanged(int state);
        void movieBoxYellowStateChanged(int state);
        void movieBoxGreenStateChanged(int state);
        void ROIaroundSegmentClicked();
        void RegistrationDirectionChanged(int state);
        void saveScreenshotClicked();
        void saveOutputFileClicked();

        // Image Checks
        void absoluteDiffClicked();
        void fiducialClicked();
        void falseColorClicked();
        void checkerboardClicked();
        void movieToggle();
        void flickerToggle();
        void flickerToggle1();

        // Vector checks
        void jacobianClicked();
        void inverseConsistClicked();
        
        // Contour checks
        void contourButtonClicked();
        
        // Parameters
        void setCheckerboardPattern(int);

protected:
	QScopedPointer<qSlicerRegistrationQualityModuleWidgetPrivate> d_ptr;
	QTimer *flickerTimer;

	virtual void setup();
	void onEnter();

private:
	Q_DECLARE_PRIVATE(qSlicerRegistrationQualityModuleWidget);
	Q_DISABLE_COPY(qSlicerRegistrationQualityModuleWidget);
};

#endif
