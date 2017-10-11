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

	// new

// 	void treeViewContextMenu(QPoint const&);
// 	void contextMenuClicked(QAction*);
// 	void loadPhaseClicked(bool);

	// end new
        void referenceVolumeChanged(vtkMRMLNode*);
        void warpedVolumeChanged(vtkMRMLNode*);

	void vectorVolumeChanged(vtkMRMLNode*);
	void invVectorVolumeChanged(vtkMRMLNode*);
	
        void outputModelChanged(vtkMRMLNode*);
	void outputDirectoyChanged();
	void ROIChanged(vtkMRMLNode*);
	void fiducialChanged(vtkMRMLNode*);
	void invFiducialChanged(vtkMRMLNode*);

	void movieBoxRedStateChanged(int state);
	void movieBoxYellowStateChanged(int state);
	void movieBoxGreenStateChanged(int state);

// 	void checkerboardVolumeChanged(vtkMRMLNode*);
// 	void absoluteDiffVolumeChanged(vtkMRMLNode*);
	
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
	
	// Parameters
	void setCheckerboardPattern(int);
	void setScalarBar2DVisibility(bool);
// 	void xmlFileNameEdited();
// 	void loadXMLClicked();
// 	void subjectHierarchyChanged(vtkMRMLNode*);

protected:
	QScopedPointer<qSlicerRegistrationQualityModuleWidgetPrivate> d_ptr;
	QTimer *flickerTimer;
	QString *lookupTableName;

	// new

// 	QMenu* contextMenu;
// 	QAction* contextMenuShowAction;

	// end new

	virtual void setup();
	void onEnter();

private:
	Q_DECLARE_PRIVATE(qSlicerRegistrationQualityModuleWidget);
	Q_DISABLE_COPY(qSlicerRegistrationQualityModuleWidget);
};

#endif
