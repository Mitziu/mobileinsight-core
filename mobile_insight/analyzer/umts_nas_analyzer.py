#!/usr/bin/python
# Filename: umts_nas_analyzer.py
"""

A UMTS NAS layer (MM/GMM/CM/SM) analyzer

Author: Yuanjie Li
Author: Zengwen Yuan
"""

try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
from analyzer import *
import timeit

from profile import Profile, ProfileHierarchy

__all__=["UmtsNasAnalyzer"]


class UmtsNasAnalyzer(Analyzer):

    """
    A protocol analyzer for UMTS NAS layer (MM/GMM/CM/SM)
    """

    def __init__(self):

        Analyzer.__init__(self)
        #init packet filters
        self.add_source_callback(self.__nas_filter)

    def set_source(self,source):
        """
        Set the trace source. Enable the LTE NAS messages.

        :param source: the trace source (collector).
        """
        Analyzer.set_source(self,source)
        #Enable MM/GMM/CM/SM logs
        source.enable_log("UMTS_NAS_OTA")
        source.enable_log("UMTS_NAS_GMM_State")
        source.enable_log("UMTS_NAS_MM_State")

    def __nas_filter(self,msg):

        """
        Filter all NAS(MM/GMM/CM/SM) packets, and call functions to process it

        :param msg: the event (message) from the trace collector.
        """

        if msg.type_id == "UMTS_NAS_MM_State":
            log_item = msg.data.decode()
            log_item_dict = dict(log_item)
            raw_msg = Event(msg.timestamp,msg.type_id,log_item_dict)
            self.__callback_mm_state(raw_msg)
    
        if msg.type_id == "UMTS_NAS_GMM_State":
            log_item = msg.data.decode()
            log_item_dict = dict(log_item)
            raw_msg = Event(msg.timestamp,msg.type_id,log_item_dict)
            self.__callback_gmm_state(raw_msg)

        if msg.type_id == "UMTS_NAS_OTA":
            # log_item = msg.data
            log_item = msg.data.decode()
            log_item_dict = dict(log_item)

            # if not log_item_dict.has_key('Msg'):
            if 'Msg' not in log_item_dict:
                return

            #Convert msg to xml format
            log_xml = ET.XML(log_item_dict['Msg'])
            xml_msg = Event(msg.timestamp,msg.type_id,log_xml)
            self.__callback_nas(xml_msg)

    def __callback_mm_state(self,msg):
        """
        Given the MM message, update MM state and substate.

        :param msg: the NAS signaling message that carries MM state
        """
        self.__mm_status.state = msg.data["MM State"]
        self.__mm_status.substate = msg.data["MM Substate"]
        self.__mm_status.update_status = msg.data["MM Update Status"]

    def __callback_gmm_state(self,msg):
        """
        Given the GMM message, update GMM state and substate.

        :param msg: the NAS signaling message that carries GMM state
        """
        ''' Sample
        2015-11-14 18:06:47.446913:UMTS_NAS_GMM_State
        <dm_log_packet><pair key="type_id">UMTS_NAS_GMM_State</pair><pair key="timestamp">2015-11-15 01:49:26.380084</pair><pair key="GMM State">GMM_DEREGISTERED</pair><pair key="GMM Substate">GMM_PLMN_SEARCH</pair><pair key="GMM Update Status">GMM_GU1_UPDATED</pair></dm_log_packet>
        MsgLogger UMTS_NAS_GMM_State 3.57007980347
        '''
        self.__gmm_status.state = msg.data['GMM State']
        self.__gmm_status.substate = msg.data['GMM Substate']
        self.__gmm_status.update_status = msg.data['GMM Update Status']

    def __callback_nas(self,msg):
        """
        Extrace MM status and configurations from the NAS messages

        :param msg: the MM NAS message
        """

        # for proto in msg.data.iter('proto'):
        #     if proto.get('name') == "gsm_a.dtap": #GSM A-I/F DTAP - Location Updating Request
        for field in proto.iter('field'):
            if field.get('show') == "DRX Parameter"
                field_val = {}

                # Default value setting
                field_val["gsm_a.gm.gmm.split_pg_cycle_code"] = None
                field_val["gsm_a.gm.gmm.cn_spec_drx_cycle_len_coef"] = None
                field_val["gsm_a.gm.gmm.split_on_ccch"] = None
                field_val["gsm_a.gm.gmm.non_drx_timer"] = None

                for val in field.iter('field'):
                    field_val[val.get('name')] = val.get('show')

                self.__mm_nas_status.drx.split_pg_cycle_code = field_val["gsm_a.gm.gmm.split_pg_cycle_code"]
                self.__mm_nas_status.drx.cn_spec_drx_cycle_len_coef = field_val["gsm_a.gm.gmm.cn_spec_drx_cycle_len_coef"]
                self.__mm_nas_status.drx.split_on_ccch = field_val["gsm_a.gm.gmm.split_on_ccch"]
                self.__mm_nas_status.drx.non_drx_timer = field_val["gsm_a.gm.gmm.non_drx_timer"]

            if field.get('show') == "Quality Of Service - Negotiated QoS":
                field_val = {}

                # Default value setting
                field_val['gsm_a.len'] = None
                field_val["gsm_a.spare_bits"] = None
                field_val["gsm_a.gm.sm.qos.delay_cls"] = None
                field_val["gsm_a.gm.sm.qos.reliability_cls"] = None
                field_val["gsm_a.gm.sm.qos.peak_throughput"] = None
                field_val["gsm_a.spare_bits"] = None
                field_val["gsm_a.gm.sm.qos.prec_class"] = None
                field_val["gsm_a.spare_bits"] = None
                field_val["gsm_a.gm.sm.qos.mean_throughput"] = None
                field_val["gsm_a.gm.sm.qos.traffic_cls"] = None
                field_val["gsm_a.gm.sm.qos.del_order"] = None
                field_val["gsm_a.gm.sm.qos.del_of_err_sdu"] = None
                field_val["gsm_a.gm.sm.qos.max_sdu"] = None
                field_val["gsm_a.gm.sm.qos.max_bitrate_upl"] = None
                field_val["gsm_a.gm.sm.qos.max_bitrate_downl"] = None
                field_val["gsm_a.gm.sm.qos.ber"] = None
                field_val["gsm_a.gm.sm.qos.sdu_err_rat"] = None
                field_val["gsm_a.gm.sm.qos.trans_delay"] = None
                field_val["gsm_a.gm.sm.qos.traff_hdl_pri"] = None
                field_val["gsm_a.gm.sm.qos.guar_bitrate_upl"] = None
                field_val["gsm_a.gm.sm.qos.guar_bitrate_downl" = None
                field_val["gsm_a.spare_bits"] = None
                field_val["gsm_a.gm.sm.qos.signalling_ind"] = None
                field_val["gsm_a.gm.sm.qos.source_stat_desc"] = None
                field_val["gsm_a.gm.sm.qos.max_bitrate_downl_ext"] = None
                field_val["gsm_a.gm.sm.qos.guar_bitrate_downl_ext"] = None

                for val in field.iter('field'):
                    field_val[val.get('name')] = val.get('show')
                    if "Maximum SDU size" in val.get('show'):
                        field_val["gsm_a.gm.`sm.qos.max_sdu"] = val.get('value')

                self.__mm_nas_status.qos_negotiated.len = field_val["gsm_a.len"]
                self.__mm_nas_status.qos_negotiated.spare_bits = field_val["gsm_a.spare_bits"]
                self.__mm_nas_status.qos_negotiated.delay_cls = field_val["gsm_a.gm.sm.qos.delay_cls"]
                self.__mm_nas_status.qos_negotiated.reliability_cls = field_val["gsm_a.gm.sm.qos.reliability_cls"]
                self.__mm_nas_status.qos_negotiated.peak_throughput = field_val["gsm_a.gm.sm.qos.peak_throughput"]
                self.__mm_nas_status.qos_negotiated.spare_bits = field_val["gsm_a.spare_bits"]
                self.__mm_nas_status.qos_negotiated.prec_class = field_val["gsm_a.gm.sm.qos.prec_class"]
                self.__mm_nas_status.qos_negotiated.spare_bits = field_val["gsm_a.spare_bits"]
                self.__mm_nas_status.qos_negotiated.mean_throughput = field_val["gsm_a.gm.sm.qos.mean_throughput"]
                self.__mm_nas_status.qos_negotiated.traffic_cls = field_val["gsm_a.gm.sm.qos.traffic_cls"]
                self.__mm_nas_status.qos_negotiated.del_order = field_val["gsm_a.gm.sm.qos.del_order"]
                self.__mm_nas_status.qos_negotiated.del_of_err_sdu = field_val["gsm_a.gm.sm.qos.del_of_err_sdu"]
                self.__mm_nas_status.qos_negotiated.max_sdu = field_val["gsm_a.gm.sm.qos.max_sdu"]
                self.__mm_nas_status.qos_negotiated.max_bitrate_upl = field_val["gsm_a.gm.sm.qos.max_bitrate_upl"]
                self.__mm_nas_status.qos_negotiated.max_bitrate_downl = field_val["gsm_a.gm.sm.qos.max_bitrate_downl"]
                self.__mm_nas_status.qos_negotiated.ber = field_val["gsm_a.gm.sm.qos.ber"]
                self.__mm_nas_status.qos_negotiated.sdu_err_rat = field_val["gsm_a.gm.sm.qos.sdu_err_rat"]
                self.__mm_nas_status.qos_negotiated.trans_delay = field_val["gsm_a.gm.sm.qos.trans_delay"]
                self.__mm_nas_status.qos_negotiated.traff_hdl_pri = field_val["gsm_a.gm.sm.qos.traff_hdl_pri"]
                self.__mm_nas_status.qos_negotiated.guar_bitrate_upl = field_val["gsm_a.gm.sm.qos.guar_bitrate_upl"]
                self.__mm_nas_status.qos_negotiated.guar_bitrate_downl = field_val["gsm_a.gm.sm.qos.guar_bitrate_downl"]
                self.__mm_nas_status.qos_negotiated.spare_bits = field_val["gsm_a.spare_bits"]
                self.__mm_nas_status.qos_negotiated.signalling_ind = field_val["gsm_a.gm.sm.qos.signalling_ind"]
                self.__mm_nas_status.qos_negotiated.source_stat_desc = field_val["gsm_a.gm.sm.qos.source_stat_desc"]
                self.__mm_nas_status.qos_negotiated.max_bitrate_downl_ext = field_val["gsm_a.gm.sm.qos.max_bitrate_downl_ext"]
                self.__mm_nas_status.qos_negotiated.guar_bitrate_downl_ext = field_val["gsm_a.gm.sm.qos.guar_bitrate_downl_ext"]

            if "Mobile Identity - TMSI/P-TMSI" in field.get('show'):
                field_val = {}

                # Default value setting
                field_val["gsm_a.len"] = None
                field_val["gsm_a.unused"] = None 
                field_val["gsm_a.oddevenind"] = None
                field_val["gsm_a.ie.mobileid.type"] = None
                field_val["gsm_a.tmsi"] = None

                for val in field.iter('field'):
                    field_val[val.get('name')] = val.get('show')

                self.__mm_nas_status.tmsi.len = field_val["gsm_a.len"]
                self.__mm_nas_status.tmsi.unused = field_val["gsm_a.unused"]
                self.__mm_nas_status.tmsi.oddevenind = field_val["gsm_a.oddevenind"]
                self.__mm_nas_status.tmsi.mobileid = field_val["gsm_a.ie.mobileid.type"]
                self.__mm_nas_status.tmsi.tmsi = field_val["gsm_a.tmsi"]

            if field.get('show') == "Quality Of Service - Requested QoS":
                field_val = {}

                # Default value setting
                field_val["gsm_a.len"] = None
                field_val["gsm_a.spare_bits"] = None
                field_val["gsm_a.gm.sm.qos.delay_cls"] = None
                field_val["gsm_a.gm.sm.qos.reliability_cls"] = None
                field_val["gsm_a.gm.sm.qos.peak_throughput"] = None
                field_val["gsm_a.spare_bits"] = None
                field_val["gsm_a.gm.sm.qos.prec_class"] = None
                field_val["gsm_a.spare_bits"] = None
                field_val["gsm_a.gm.sm.qos.mean_throughput"] = None
                field_val["gsm_a.gm.sm.qos.traffic_cls"] = None
                field_val["gsm_a.gm.sm.qos.del_order"] = None
                field_val["gsm_a.gm.sm.qos.del_of_err_sdu"] = None
                field_val["gsm_a.gm.sm.qos.max_sdu"] = None
                field_val["gsm_a.gm.sm.qos.max_bitrate_upl"] = None
                field_val["gsm_a.gm.sm.qos.max_bitrate_downl"] = None
                field_val["gsm_a.gm.sm.qos.ber"] = None
                field_val["gsm_a.gm.sm.qos.sdu_err_rat"] = None
                field_val["gsm_a.gm.sm.qos.trans_delay"] = None
                field_val["gsm_a.gm.sm.qos.traff_hdl_pri"] = None
                field_val["gsm_a.gm.sm.qos.guar_bitrate_upl"] = None
                field_val["gsm_a.gm.sm.qos.guar_bitrate_downl" = None
                field_val["gsm_a.spare_bits"] = None
                field_val["gsm_a.gm.sm.qos.signalling_ind"] = None
                field_val["gsm_a.gm.sm.qos.source_stat_desc"] = None
                field_val["gsm_a.gm.sm.qos.max_bitrate_downl_ext"] = None
                field_val["gsm_a.gm.sm.qos.guar_bitrate_downl_ext"] = None

                for val in field.iter('field'):
                    field_val[val.get('name')] = val.get('show')
                    if "Maximum SDU size" in val.get('show'):
                        field_val["gsm_a.gm.sm.qos.max_sdu"] = val.get('value')

                self.__mm_nas_status.qos_requested.len = field_val["gsm_a.len"]
                self.__mm_nas_status.qos_requested.spare_bits = field_val["gsm_a.spare_bits"]
                self.__mm_nas_status.qos_requested.delay_cls = field_val["gsm_a.gm.sm.qos.delay_cls"]
                self.__mm_nas_status.qos_requested.reliability_cls = field_val["gsm_a.gm.sm.qos.reliability_cls"]
                self.__mm_nas_status.qos_requested.peak_throughput = field_val["gsm_a.gm.sm.qos.peak_throughput"]
                self.__mm_nas_status.qos_requested.spare_bits = field_val["gsm_a.spare_bits"]
                self.__mm_nas_status.qos_requested.prec_class = field_val["gsm_a.gm.sm.qos.prec_class"]
                self.__mm_nas_status.qos_requested.spare_bits = field_val["gsm_a.spare_bits"]
                self.__mm_nas_status.qos_requested.mean_throughput = field_val["gsm_a.gm.sm.qos.mean_throughput"]
                self.__mm_nas_status.qos_requested.traffic_cls = field_val["gsm_a.gm.sm.qos.traffic_cls"]
                self.__mm_nas_status.qos_requested.del_order = field_val["gsm_a.gm.sm.qos.del_order"]
                self.__mm_nas_status.qos_requested.del_of_err_sdu = field_val["gsm_a.gm.sm.qos.del_of_err_sdu"]
                self.__mm_nas_status.qos_requested.max_sdu = field_val["gsm_a.gm.sm.qos.max_sdu"]
                self.__mm_nas_status.qos_requested.max_bitrate_upl = field_val["gsm_a.gm.sm.qos.max_bitrate_upl"]
                self.__mm_nas_status.qos_requested.max_bitrate_downl = field_val["gsm_a.gm.sm.qos.max_bitrate_downl"]
                self.__mm_nas_status.qos_requested.ber = field_val["gsm_a.gm.sm.qos.ber"]
                self.__mm_nas_status.qos_requested.sdu_err_rat = field_val["gsm_a.gm.sm.qos.sdu_err_rat"]
                self.__mm_nas_status.qos_requested.trans_delay = field_val["gsm_a.gm.sm.qos.trans_delay"]
                self.__mm_nas_status.qos_requested.traff_hdl_pri = field_val["gsm_a.gm.sm.qos.traff_hdl_pri"]
                self.__mm_nas_status.qos_requested.guar_bitrate_upl = field_val["gsm_a.gm.sm.qos.guar_bitrate_upl"]
                self.__mm_nas_status.qos_requested.guar_bitrate_downl = field_val["gsm_a.gm.sm.qos.guar_bitrate_downl"]
                self.__mm_nas_status.qos_requested.spare_bits = field_val["gsm_a.spare_bits"]
                self.__mm_nas_status.qos_requested.signalling_ind = field_val["gsm_a.gm.sm.qos.signalling_ind"]
                self.__mm_nas_status.qos_requested.source_stat_desc = field_val["gsm_a.gm.sm.qos.source_stat_desc"]
                self.__mm_nas_status.qos_requested.max_bitrate_downl_ext = field_val["gsm_a.gm.sm.qos.max_bitrate_downl_ext"]
                self.__mm_nas_status.qos_requested.guar_bitrate_downl_ext = field_val["gsm_a.gm.sm.qos.guar_bitrate_downl_ext"]

            # TODO:
            # show="MS Network Capability"
            # show="Attach Type"
            # show="MS Radio Access Capability"
            # show="GPRS Timer - Ready Timer"
            # show="P-TMSI type"
            # show="Routing Area Identification - Old routing area identification - RAI: 310-260-26281-1"