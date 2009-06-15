package org.jythonbook;

public class Main {

    public static void main(String args[]) {
        // what other control options should we provide to the factory?
        // jsr223 might have some good ideas, but also let's keep some simple code usage
        // for now, let's just try out and refine
        JythonObjectFactory factory = new JythonObjectFactory(
                BuildingType.class, "building", "Building");

        BuildingType building = (BuildingType) factory.createObject();

        building.setBuildingName("BUIDING-A");
        building.setBuildingAddress("100 MAIN ST.");
        building.setBuildingId(1);

        System.out.println(building.getBuildingId() + " " + building.getBuildingName() + " " +
                building.getBuildingAddress());
    }
}