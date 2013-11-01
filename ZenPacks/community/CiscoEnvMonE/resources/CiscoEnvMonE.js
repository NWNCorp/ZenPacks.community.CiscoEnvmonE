(function(){

var ZC = Ext.ns('Zenoss.component');

ZC.registerName('CiscoEnvMonFan', _t('Fan (envmon)'), _t('Fans (envmon)'));
ZC.registerName('CiscoEnvMonTemperatureSensor', _t('Temperature Sensor( envmon)'), _t('Temperature Sensors (envmon)'));
ZC.registerName('CiscoEnvMonPowerSupply', _t('Power Supply (envmon)'), _t('Power Supplies (envmon)'));
ZC.registerName('CiscoEnvMonVoltageSensor', _t('Voltage Sensor'), _t('Voltage Sensors'));

ZC.CiscoEnvMonFanPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CiscoEnvMonFan',
            autoExpandColumn: 'name',
            sortInfo: {
                field: 'name',
                direction: 'asc',
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'meta_type'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name')
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                width: 60
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });
        ZC.CiscoEnvMonFanPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CiscoEnvMonFanPanel', ZC.CiscoEnvMonFanPanel);

ZC.CiscoEnvMonTemperatureSensorPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CiscoEnvMonTemperatureSensor',
            autoExpandColumn: 'name',
            sortInfo: {
                field: 'name',
                direction: 'asc',
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'meta_type'},
                {name: 'temp_threshold_string'},
                {name: 'temp_lastshutdown_string'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'StatsDescr'},
                {name: 'locking'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true,
            },{
                id: 'temp_threshold_string',
                dataIndex: 'temp_threshold_string',
                header: _t('Shut-down threshold'),
                width: 200
            },{
                id: 'temp_lastshutdown_string',
                dataIndex: 'temp_lastshutdown_string',
                header: _t('Temp at last thermal shut-down'),
                width: 200
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 100,
                sortable: true
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60,
                renderer: Zenoss.render.checkbox,
                sortable: true
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });
        ZC.CiscoEnvMonTemperatureSensorPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CiscoEnvMonTemperatureSensorPanel', ZC.CiscoEnvMonTemperatureSensorPanel);

ZC.CiscoEnvMonPowerSupplyPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CiscoEnvMonPowerSupply',
            autoExpandColumn: 'name',
            sortInfo: {
                field: 'name',
                direction: 'asc',
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'meta_type'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'supply_source'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'StatsDescr'},
                {name: 'locking'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60,
                sortable: true
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
            },{
                id: 'supply_source',
                dataIndex: 'supply_source',
                header: _t('Power Supply Source'),
                width: 100,
                sortable: true
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60,
                renderer: Zenoss.render.checkbox,
                sortable: true
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 100,
                sortable: true
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });
        ZC.CiscoEnvMonPowerSupplyPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CiscoEnvMonPowerSupplyPanel', ZC.CiscoEnvMonPowerSupplyPanel);

ZC.CiscoEnvMonVoltageSensorPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CiscoEnvMonVoltageSensor',
            autoExpandColumn: 'name',
            sortInfo: {
                field: 'name',
                direction: 'asc',
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'meta_type'},
                {name: 'combined_shutdown_thresholds_string'},
                {name: 'voltage_last_shutdown'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'StatsDescr'},
                {name: 'locking'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60,
                sortable: true
             },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
             },{
                id: 'combined_shutdown_thresholds_string',
                dataIndex: 'combined_shutdown_thresholds_string',
                header: _t('(Low/High) Shutdown Tolerances'),
                width: 200
             },{
                id: 'voltage_last_shutdown',
                dataIndex: 'voltage_last_shutdown',
                header: _t('Voltage at last emergency shut-down'),
                width: 200
             },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 150,
                sortable: true
             },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                width: 60
             },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });
        ZC.CiscoEnvMonVoltageSensorPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CiscoEnvMonVoltageSensorPanel', ZC.CiscoEnvMonVoltageSensorPanel);

})();
