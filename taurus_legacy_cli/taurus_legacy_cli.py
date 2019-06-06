# -*- coding: utf-8 -*-

"""Main module."""

import sys

import taurus
from taurus.qt.qtgui.application import TaurusApplication
from taurus.core.util import argparse
from taurus import Release


def taurusconfigeditor():
    from taurus.qt.qtgui.panel.taurusconfigeditor import QConfigEditor

    parser = argparse.get_taurus_parser()
    parser.set_usage("%prog [options] [INIFILENAME]")
    parser.set_description("taurus configuration editor")
    app = TaurusApplication(cmd_line_parser=parser,
                            app_name="taurusconfigeditor",
                            app_version=Release.version)
    args = app.get_command_line_args()
    w = QConfigEditor()
    w.setMinimumSize(500, 500)
    w.show()
    if len(args) == 1:
        w.loadFile(args[0])
    sys.exit(app.exec_())


def taurusplot():
    import datetime
    from taurus.qt.qtgui.qwt5 import TaurusPlot

    parser = argparse.get_taurus_parser()
    parser.set_usage("%prog [options] [<model1> [<model2>] ...]")
    parser.set_description("a taurus application for plotting 1D data sets")
    parser.add_option("-x", "--x-axis-mode", dest="x_axis_mode", default='e',
                      metavar="t|n",
                      help="interprete X values as either timestamps (t) or numbers (n). Accepted values: t|n (e is also accepted as a synonim of n)")
    parser.add_option("--config", "--config-file", dest="config_file",
                      default=None,
                      help="use the given config file for initialization")
    parser.add_option("--import-ascii", dest="import_ascii", default=None,
                      help="import the given ascii file into the plot")
    parser.add_option("--export", "--export-file", dest="export_file",
                      default=None,
                      help="use the given file to as output instead of showing the plot")
    parser.add_option("--window-name", dest="window_name",
                      default="TaurusPlot", help="Name of the window")

    app = TaurusApplication(cmd_line_parser=parser, app_name="taurusplot",
                            app_version=Release.version)
    args = app.get_command_line_args()
    options = app.get_command_line_options()
    if options.x_axis_mode.lower() not in ['t', 'e', 'n']:
        parser.print_help(sys.stderr)
        sys.exit(1)

    models = args
    w = TaurusPlot()
    w.setWindowTitle(options.window_name)

    w.setXIsTime(options.x_axis_mode.lower() == 't')
    if options.config_file is not None:
        w.loadConfig(options.config_file)

    if options.import_ascii is not None:
        w.importAscii([options.import_ascii], xcol=0)

    if models:
        w.setModel(models)

    if options.export_file is not None:
        curves = dict.fromkeys(w.trendSets, 0)

        def exportIfAllCurves(curve, trend=w, counters=curves):
            curve = str(curve)
            print('*' * 10 + ' %s: Event received for %s  ' % (
                datetime.now().isoformat(), curve) + '*' * 10)
            if curve in counters:
                counters[curve] += 1
                if all(counters.values()):
                    trend.exportPdf(options.export_file)
                    print('*' * 10 + ' %s: Exported to : %s  ' % (
                        datetime.now().isoformat(),
                        options.export_file) + '*' * 10)
                    trend.close()
            return

        if not curves:
            w.close()
        else:
            for ts in w.trendSets.values():
                ts.dataChanged.connect(exportIfAllCurves)
        sys.exit(app.exec_())  # exit without showing the widget

    # show the widget
    w.show()
    # if no models are passed, show the data import dialog
    if (len(models) == 0
        and options.config_file is None
        and options.import_ascii is None
    ):
        w.showDataImportDlg()

    sys.exit(app.exec_())


def taurustrend():
    from taurus.qt.qtgui.qwt5 import TaurusTrend
    import datetime

    parser = argparse.get_taurus_parser()
    parser.set_usage("%prog [options] [<model1> [<model2>] ...]")
    parser.set_description("a taurus application for plotting trends")
    parser.add_option("-x", "--x-axis-mode", dest="x_axis_mode", default='t',
                      metavar="t|e",
                      help="interprete X values as either timestamps (t) or event numbers (e). Accepted values: t|e")
    parser.add_option("-b", "--buffer", dest="max_buffer_size",
                      default=TaurusTrend.DEFAULT_MAX_BUFFER_SIZE,
                      help="maximum number of values per curve to be plotted (default = %i) (when reached, the oldest values will be discarded)" % TaurusTrend.DEFAULT_MAX_BUFFER_SIZE)
    parser.add_option("--config", "--config-file", dest="config_file",
                      default=None,
                      help="use the given config file for initialization")
    parser.add_option("--export", "--export-file", dest="export_file",
                      default=None,
                      help="use the given file to as output instead of showing the plot")
    parser.add_option("-r", "--forced-read", dest="forced_read_period",
                      type="int", default=-1, metavar="MILLISECONDS",
                      help="force Taurustrend to re-read the attributes every MILLISECONDS ms")
    parser.add_option("-a", "--use-archiving",
                      action="store_true", dest="use_archiving", default=False)
    parser.add_option("--window-name", dest="window_name",
                      default="TaurusTrend", help="Name of the window")

    app = TaurusApplication(cmd_line_parser=parser, app_name="taurustrend",
                            app_version=Release.version)
    args = app.get_command_line_args()
    options = app.get_command_line_options()
    if options.x_axis_mode.lower() not in ['t', 'e']:
        parser.print_help(sys.stderr)
        sys.exit(1)

    models = args

    w = TaurusTrend()
    w.setWindowTitle(options.window_name)

    # xistime option
    w.setXIsTime(options.x_axis_mode.lower() == 't')
    # max buffer size option
    w.setMaxDataBufferSize(int(options.max_buffer_size))
    # configuration file option
    if options.config_file is not None:
        w.loadConfig(options.config_file)
    # set models
    if models:
        w.setModel(models)
    # export option
    if options.export_file is not None:
        curves = dict.fromkeys(w.trendSets, 0)

        def exportIfAllCurves(curve, trend=w, counters=curves):
            curve = str(curve)
            print('*' * 10 + ' %s: Event received for %s  ' % (
            datetime.now().isoformat(), curve) + '*' * 10)
            if curve in counters:
                counters[curve] += 1
                if all(counters.values()):
                    trend.exportPdf(options.export_file)
                    print('*' * 10 + ' %s: Exported to : %s  ' % (
                    datetime.now().isoformat(), options.export_file) + '*' * 10)
                    trend.close()
            return

        if not curves:
            w.close()
        else:
            for ts in w.trendSets.values():
                ts.dataChanged.connect(exportIfAllCurves)
        sys.exit(app.exec_())  # exit without showing the widget

    # period option
    if options.forced_read_period > 0:
        w.setForcedReadingPeriod(options.forced_read_period)

    # archiving option
    w.setUseArchiving(options.use_archiving)

    # show the widget
    w.show()

    # if no models are passed, show the data import dialog
    if len(models) == 0 and options.config_file is None:
        w.showDataImportDlg()

    sys.exit(app.exec_())


def taurusFormMain():
    """A launcher for TaurusForm."""

    from taurus.qt.qtgui.panel import TaurusForm
    from taurus.external.qt import Qt
    from functools import partial

    parser = argparse.get_taurus_parser()
    parser.set_usage("%prog [options] [model1 [model2 ...]]")
    parser.set_description("the taurus form panel application")
    parser.add_option("--window-name", dest="window_name",
                      default="TaurusForm", help="Name of the window")
    parser.add_option("--config", "--config-file", dest="config_file",
                      default=None,
                      help="use the given config file for initialization")
    app = TaurusApplication(cmd_line_parser=parser,
                            app_name="taurusform",
                            app_version=Release.version)
    args = app.get_command_line_args()
    options = app.get_command_line_options()

    dialog = TaurusForm()
    dialog.setModifiableByUser(True)
    dialog.setModelInConfig(True)
    dialog.setWindowTitle(options.window_name)

    # Make sure the window size and position are restored
    dialog.registerConfigProperty(dialog.saveGeometry, dialog.restoreGeometry,
                                  'MainWindowGeometry')

    quitApplicationAction = Qt.QAction(
        Qt.QIcon.fromTheme("process-stop"), 'Close Form', dialog)
    quitApplicationAction.triggered.connect(dialog.close)

    saveConfigAction = Qt.QAction("Save current settings...", dialog)
    saveConfigAction.setShortcut(Qt.QKeySequence.Save)
    saveConfigAction.triggered.connect(
        partial(dialog.saveConfigFile, ofile=None))
    loadConfigAction = Qt.QAction("&Retrieve saved settings...", dialog)
    loadConfigAction.setShortcut(Qt.QKeySequence.Open)
    loadConfigAction.triggered.connect(
        partial(dialog.loadConfigFile, ifile=None))

    dialog.addActions(
        (saveConfigAction, loadConfigAction, quitApplicationAction))

    # set the default map for this installation
    from taurus import tauruscustomsettings
    dialog.setCustomWidgetMap(
        getattr(tauruscustomsettings, 'T_FORM_CUSTOM_WIDGET_MAP', {}))

    # set a model list from the command line or launch the chooser
    if options.config_file is not None:
        dialog.loadConfigFile(options.config_file)
    elif len(args) > 0:
        models = args
        dialog.setModel(models)
    else:
        dialog.chooseModels()

    dialog.show()

    sys.exit(app.exec_())


def TaurusDevicePanelMain():
    """A launcher for TaurusDevicePanel."""
    from taurus.qt.qtgui.panel import TaurusDevicePanel
    from taurus.core.taurusbasetypes import TaurusElementType

    parser = argparse.get_taurus_parser()
    parser.set_usage("%prog [options] [devname [attrs]]")
    parser.set_description("Taurus Application inspired in Jive and Atk Panel")
    parser.add_option("", "--config-file", dest="config_file", default=None,
                      help="load a config file (TODO: document this option)")

    app = TaurusApplication(cmd_line_parser=parser,
                            app_name="TaurusDevicePanel",
                            app_version=Release.version)
    args = app.get_command_line_args()
    options = app.get_command_line_options()

    w = TaurusDevicePanel()
    w.show()

    if len(args) == 0:
        from taurus.qt.qtgui.panel import TaurusModelChooser
        models, ok = TaurusModelChooser.modelChooserDlg(
            w, selectables=[TaurusElementType.Member], singleModel=True
        )
        model = models[0] if ok and models else None
        filters = ''
    else:
        model = args[0]
        filters = args[1:]

    if options.config_file is not None:
        w.loadConfigFile(options.config_file)
    elif model and filters:
        w.setAttributeFilters({model: filters})

    w.setModel(model)

    sys.exit(app.exec_())


def TaurusPanelMain():
    """A launcher for TaurusPanel."""

    from taurus.qt.qtgui.panel import TaurusDevPanel

    parser = argparse.get_taurus_parser()
    parser.set_usage("%prog [options] [devname]")
    parser.set_description("Taurus Application inspired in Jive and Atk Panel")

    app = TaurusApplication(cmd_line_parser=parser, app_name="tauruspanel",
                            app_version=Release.version)
    args = app.get_command_line_args()
    options = app.get_command_line_options()

    w = TaurusDevPanel()

    if options.tango_host is None:
        options.tango_host = taurus.Authority().getNormalName()
    w.setTangoHost(options.tango_host)

    if len(args) == 1:
        w.setDevice(args[0])

    w.show()

    sys.exit(app.exec_())


def taurusgui(confname=None):
    from taurus.qt.qtgui.taurusgui import TaurusGui

    taurus.info('Starting execution of TaurusGui')

    parser = argparse.get_taurus_parser()
    parser.set_usage("%prog [options] confname")
    parser.set_description("The taurus GUI application")
    parser.add_option(
        "", "--config-dir", dest="config_dir", default=None,
        help="use the given configuration directory for initialization")
    parser.add_option(
        "", "--new-gui", action="store_true", dest="new_gui", default=None,
        help="launch a wizard for creating a new TaurusGUI application")
    parser.add_option(
        "", "--fail-proof", action="store_true", dest="fail_proof",
        default=None,
        help="launch in fail proof mode (it prevents potentially problematic configs from being loaded)")

    app = TaurusApplication(cmd_line_parser=parser, app_name="taurusgui",
                            app_version=taurus.Release.version)
    args = app.get_command_line_args()
    options = app.get_command_line_options()

    if options.new_gui:  # launch app settings wizard instead of taurusgui
        from taurus.qt.qtgui.taurusgui import AppSettingsWizard
        wizard = AppSettingsWizard()
        wizard.show()
        sys.exit(app.exec_())

    if confname is None:
        confname = options.config_dir

    if confname is None:
        if len(
            args) == 1:  # for backwards compat, we allow to specify the confname without the "--config-dir" parameter
            confname = args[0]
        else:
            parser.print_help(sys.stderr)
            sys.exit(1)

    if options.fail_proof:
        configRecursionDepth = 0
    else:
        configRecursionDepth = None

    gui = TaurusGui(None, confname=confname,
                    configRecursionDepth=configRecursionDepth)

    gui.show()
    ret = app.exec_()

    taurus.info('Finished execution of TaurusGui')
    sys.exit(ret)


def taurusdesigner(env=None):
    import optparse
    from taurus.qt.qtdesigner.taurusdesigner import (get_taurus_designer_env,
                                                     qtdesigner_start)

    if env is not None:
        taurus.info('ignoring obsolete env parameter to qtdesigner_start')

    version = "taurusdesigner %s" % (Release.version)
    usage = "Usage: %prog [options] <ui file(s)>"
    description = "The Qt designer application customized for taurus"
    parser = optparse.OptionParser(
        version=version, usage=usage, description=description)
    parser.add_option(
        "--taurus-path", dest="tauruspath", default="",
        help="additional directories to look for taurus widgets"
    )
    parser.add_option(
        "--qt-designer-path", dest="pyqtdesignerpath", default="",
        help="additional directories to look for python qt widgets"
    )

    options, args = parser.parse_args()

    taurus_extra_path = None
    # Set TAURUSQTDESIGNERPATH
    if len(options.tauruspath) > 0:
        taurus_extra_path = options.tauruspath

    if env is None:
        env = get_taurus_designer_env(taurus_extra_path=taurus_extra_path)

    sys.exit(qtdesigner_start(args, env=env))


def taurusImageDlgMain():
    from taurus.qt.qtgui.extra_guiqwt.plot import TaurusImageDialog

    # prepare options
    parser = taurus.core.util.argparse.get_taurus_parser()
    parser.set_usage("%prog [options] <model>")
    parser.set_description(
        'a Taurus application for plotting Image Attributes')
    parser.add_option("--demo", action="store_true", dest="demo",
                      default=False, help="show a demo of the widget")
    parser.add_option("--rgb", action="store_true", dest="rgb_mode",
                      default=False, help="assume image is RGB")
    parser.add_option("--window-name", dest="window_name",
                      default="Taurus Image", help="Name of the window")
    app = TaurusApplication(
        cmd_line_parser=parser, app_name="Taurus Image Dialog",
        app_version=taurus.Release.version)
    args = app.get_command_line_args()
    options = app.get_command_line_options()

    # TODO:  is "--rgb --demo" doing the right thing?? Check it.
    # check & process options
    if options.demo:
        if options.rgb_mode:
            args.append('eval:randint(0,256,(10,20,3))')
        else:
            args.append('eval:rand(256,128)')
    w = TaurusImageDialog(wintitle=options.window_name)

    w.setRGBmode(options.rgb_mode)

    # set model
    if len(args) == 1:
        w.setModel(args[0])
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)

    w.show()
    sys.exit(app.exec_())


def taurusTrend2DMain():
    from taurus.qt.qtgui.extra_guiqwt.taurustrend2d import TaurusTrend2DDialog

    # prepare options
    parser = taurus.core.util.argparse.get_taurus_parser()
    parser.set_usage("%prog [options] <model>")
    parser.set_description('a Taurus application for plotting trends of ' +
                           'arrays (aka "spectrograms")')
    parser.add_option("-x", "--x-axis-mode", dest="x_axis_mode", default='d',
                      metavar="t|d|e",
                      help=("interpret X values as timestamps (t), " +
                            "time deltas (d) or event numbers (e). " +
                            "Accepted values: t|d|e")
                      )
    parser.add_option("-b", "--buffer", dest="max_buffer_size", default='512',
                      help=("maximum number of values to be stacked " +
                            "(when reached, the oldest values will be " +
                            "discarded)")
                      )
    parser.add_option("-a", "--use-archiving",
                      action="store_true", dest="use_archiving", default=False)
    parser.add_option("--demo", action="store_true", dest="demo",
                      default=False, help="show a demo of the widget")
    parser.add_option("--window-name", dest="window_name",
                      default="Taurus Trend 2D", help="Name of the window")

    app = TaurusApplication(cmd_line_parser=parser, app_name="Taurus Trend 2D",
                            app_version=taurus.Release.version)
    args = app.get_command_line_args()
    options = app.get_command_line_options()

    # check & process options
    stackModeMap = dict(t='datetime', d='deltatime', e='event')
    if options.x_axis_mode.lower() not in stackModeMap:
        parser.print_help(sys.stderr)
        sys.exit(1)

    stackMode = stackModeMap[options.x_axis_mode.lower()]

    if options.demo:
        args.append('eval:x=linspace(0,3,40);t=rand();sin(x+t)')

    w = TaurusTrend2DDialog(stackMode=stackMode, wintitle=options.window_name,
                            buffersize=int(options.max_buffer_size))

    # set archiving
    if options.use_archiving:
        raise NotImplementedError('Archiving support is not yet implemented')
        w.setUseArchiving(True)

    # set model
    if len(args) == 1:
        w.setModel(args[0])
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)

    w.show()
    sys.exit(app.exec_())


def taurusdemo():
    from taurus.qt.qtgui.panel.taurusdemo import TaurusDemoPanel

    parser = taurus.core.util.argparse.get_taurus_parser()
    parser.set_description("A demo application for taurus")
    app = taurus.qt.qtgui.application.TaurusApplication(
        cmd_line_parser=parser, app_name="taurusdemo", app_version="1.0",
        org_domain="Taurus", org_name="Tango community")
    gui = TaurusDemoPanel()
    gui.setWindowTitle(app.applicationName())
    gui.show()
    sys.exit(app.exec_())
