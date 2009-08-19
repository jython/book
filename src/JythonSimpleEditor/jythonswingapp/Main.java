/**
 * Main.java
 *
 * This implementation of the Main class uses the PythonInterpreter to drive
 * the simple Jython editor GUI
 *
 * J Juneau
 */

package jythonswingapp;

import org.python.core.PyException;
import org.python.util.PythonInterpreter;

public class Main {
    public static void main(String[] args) throws PyException{
	PythonInterpreter intrp = new PythonInterpreter();
	intrp.exec("import JythonSimpleSwing as jy");
	intrp.exec("jy.JythonSimpleSwing().start()");
    }
}