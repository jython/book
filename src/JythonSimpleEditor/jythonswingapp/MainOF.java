/**
 * Main.java
 *
 * This implementation of the Main class uses the object factory technique to drive
 * the simple Jython editor GUI
 *
 * J Juneau
 */

package jythonswingapp;

import jythonswingapp.interfaces.JySwingType;
import org.plyjy.factory.JythonObjectFactory;


public class MainOF {

    /**
     * @param args the command line arguments
     */

    JythonObjectFactory factory;

    public static void invokeJython(){

        JySwingType jySwing = (JySwingType) JythonObjectFactory
                .createObject(JySwingType.class, "JythonSimpleSwing");
        jySwing.start();
    }

    public static void main(String[] args) {
        invokeJython();
    }

}
