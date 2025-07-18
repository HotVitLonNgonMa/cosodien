import csv
import os
import math as m
import pathlib as pl
import pandas as pd

def write_file(filename, tupl):
    f = open(f"{filename}.csv", "a", newline="")
    writer = csv.writer(f)
    writer.writerow(tupl)
    f.close()


root = pl.Path("D:/Linh Python/Cosodien/data")
option = input("Enter the directory: ")
inp = input("File's name: ")
directory = root / f"{option}"
fields = ['sample', "Vin", "Vout", "R1", "phase", "freq", "type", "length", "Z", "Re(Z)", "Im(Z)", "state"]

def filter_func(filename):
    df = pd.read_csv(filename, skiprows=28)
    drop_indices = []

    for idx in range(len(df) - 1):
        if float(df.loc[idx, "CH2 Amplitude(V)"]) < float(df.loc[idx + 1, "CH2 Amplitude(V)"]):
            drop_indices.append(idx)

    df = df.drop(index=drop_indices).reset_index(drop=True)
    return df

def create_new_file(filename):
    if os.path.exists(f"{filename}.csv") == 0 or os.path.getsize(f"{filename}.csv") == 0:
        write_file(filename, fields)
    for sample in os.listdir(directory):
        print(sample)
        sample_path = os.path.join(directory, sample)
        for date in os.listdir(sample_path):
            print(date)
            day_path = os.path.join(sample_path, date)
            for type_name in os.listdir(day_path):
                v = os.path.splitext(os.path.basename(type_name))[0]
                match(int(v[-1])):
                    case 0: t = "doc"
                    case 1: t = "ngang"
                print(t)
                type_path = os.path.join(day_path, type_name)

                df = filter_func(type_path)

                for idx, row in df.iterrows():
                    freq = row["Frequency(Hz)"]
                    Vin = 5
                    Vout = round(float(row["CH2 Amplitude(V)"]), 4)
                    phase = -round(float(row["CH2 Phase(Deg)"]), 4)
                    try:
                        phase_rad = m.radians(phase)
                        x = pow(m.cos(phase_rad) - Vout / Vin, 2) + pow(m.sin(phase_rad), 2)
                        Re_Z = 12280 * (Vout / Vin) * ((m.cos(m.radians(phase_rad)) - (Vout / Vin)) / x)
                        Im_Z = 12280 * (Vout / Vin) * (-m.sin(phase_rad) / x)
                    except(ZeroDivisionError, ValueError):
                        Re_Z = 0
                        Im_Z = 0

                    try:
                        Z = round((12280 / ((Vin / Vout) - 1)), 2)
                    except(ZeroDivisionError, ValueError):
                        Z = 0
                    row = [sample, Vin, Vout, 12280, phase, freq, t, "1cm", Z, round(Re_Z, 2), round(Im_Z , 2), date[:3]]

                    write_file(filename, row)


create_new_file(inp)