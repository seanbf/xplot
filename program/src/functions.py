import streamlit as st
import numpy as np

@st.cache
def gain(signal, gain):
    signal_gain = signal*gain
    return signal_gain

@st.cache   
def offset(signal, offset):
    signal_offset = signal + offset
    return signal_offset

@st.cache    
def rms2peak(signal_rms):
    signal_peak = signal_rms * np.sqrt(2)
    return signal_peak

@st.cache    
def peak2rms(signal_peak):
    signal_rms = signal_peak / np.sqrt(2)
    return signal_rms

@st.cache    
def rpm2rads(speed_rpm):
    speed_rads = (speed_rpm / 60) * (2 * np.pi)
    return speed_rads

@st.cache    
def rads2rpm(speed_rads):
    speed_rpm = (speed_rads / (2 * np.pi)) * 60
    return speed_rpm

@st.cache    
def degree2revs(angle_degree):
    angle_revs = angle_degree / 360
    return angle_revs

@st.cache    
def revs2degree(angle_revs):
    angle_degree = angle_revs * 360
    return angle_degree

@st.cache
def time2frequency(time):
    frequency = 1/time
    return frequency

# Functions

def y_functions_dict():
    functions = dict({
                    'gain':gain,
                    'offset':offset,
                    'rms2peak':rms2peak,
                    'peak2rms':peak2rms,
                    'rpm2rads':rpm2rads,
                    'rads2rpm':rads2rpm,
                    'degree2revs':degree2revs,
                    'revs2degree':revs2degree
                    })
    return functions