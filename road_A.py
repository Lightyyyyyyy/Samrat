from vehicle_counting import VehicleCounter

road_A = VehicleCounter("A", r"C:\\Users\\user\\OneDrive\\Desktop\\feed\\Feed 1.mp4")
road_A.process_video()
print(f"Total unique vehicles detected on Road A: {road_A.get_vehicle_count()}")