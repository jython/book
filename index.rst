.. Jython Book documentation master file, created by
   sphinx-quickstart on Wed Jun 10 21:44:59 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The Definitive Guide to Jython
==============================
Python for the Java Platform
----------------------------

:Authors: 
    Josh Juneau, 
    Jim Baker,
    Victor Ng,
    Leo Soto,
    Frank Wierzbicki

:Version: Approximately 1.0 of 03/25/2010

.. This is a partial update from Josh Juneau's repository
   at https://bitbucket.org/javajuneau/jythonbook


This book is presented in open source and licensed through Creative Commons 3.0.
You are free to copy, distribute, transmit, and/or adapt the work.  This license
is based upon the following conditions:

Attribution:

You must attribute the work in the manner specified by the author
or licensor (but not in any way that suggests that they endorse
you or your use of the work).

Share Alike:

If you alter, transform, or build upon this work, you may distribute the
resulting work only under the same, similar or a compatible license.

Any of the above conditions can be waived if you get permission from
the copyright holder.

In no way are any of the following rights affected by the license:

 - Your fair dealing or fair use rights
 - The author's moral rights
 - Rights other persons may have either in the work itself or in how
   the work is used, such as publicity or privacy rights
   
Notice:  For any reuse or distribution, you must make clear to the others
the license terms of this work.  The best way to do this is with a direct
link to this page:  http://creativecommons.org/licenses/by-sa/3.0/

Inside Cover (Apress first edition)
===================================

.. This is verbatim from Josh's repo but some of it looks out of place in the
   electronic version. OTOH, what harm does it do to to credit here people
   who contributed to the paper edition?

The Definitive Guide to Jython: Python for the Java Platform

Copyright © 2010 by Josh Juneau, Jim Baker, Victor Ng, Leo Soto, Frank Wierzbicki

All rights reserved. No part of this work may be reproduced or transmitted in any form or by any means,
electronic or mechanical, including photocopying, recording, or by any information storage or retrieval
system, without the prior written permission of the copyright owner and the publisher.

ISBN-13 (pbk): 978-1-4302-2527-0

ISBN-13 (electronic): 978-1-4302-2528-7

Printed and bound in the United States of America 9 8 7 6 5 4 3 2 1

Trademarked names may appear in this book. Rather than use a trademark symbol with every
occurrence of a trademarked name, we use the names only in an editorial fashion and to the benefit of
the trademark owner, with no intention of infringement of the trademark.

Java™ and all Java-based marks are trademarks or registered trademarks of Sun Microsystems, Inc., in
the US and other countries. Apress, Inc., is not affiliated with Sun Microsystems, Inc., and this book was
written without endorsement from Sun Microsystems, Inc.

Lead Editors: Steve Anglin, Duncan Parkes

Technical Reviewers: Mark Ramm, Tobias Ivarsson

Editorial Board: Clay Andres, Steve Anglin, Mark Beckner, Ewan Buckingham, Gary Cornell,
Jonathan Gennick, Jonathan Hassell, Michelle Lowman, Matthew Moodie, Duncan Parkes,
Jeffrey Pepper, Frank Pohlmann, Douglas Pundick, Ben Renow-Clarke, Dominic
Shakeshaft, Matt Wade, Tom Welsh

Coordinating Editor: Mary Tobin

Copy Editor: Tracy Brown Collins

Associate Production Director: Kari Brooks-Copony

Manufacturing Director: Tom Debolski

Distributed to the book trade worldwide by Springer-Verlag New York, Inc., 233 Spring Street, 6th Floor,
New York, NY 10013. Phone 1-800-SPRINGER, fax 201-348-4505, e-mail orders-ny@springer-sbm.com, or
visit http://www.springeronline.com.

For information on translations, please e-mail info@apress.com, or visit http://www.apress.com.

Apress and friends of ED books may be purchased in bulk for academic, corporate, or promotional use.
eBook versions and licenses are also available for most titles. For more information, reference our
Special Bulk Sales–eBook Licensing web page at http://www.apress.com/info/bulksales.

The information in this book is distributed on an “as is” basis, without warranty. Although every
precaution has been taken in the preparation of this work, neither the author(s) nor Apress shall have
any liability to any person or entity with respect to any loss or damage caused or alleged to be caused
directly or indirectly by the information contained in this work.
This book is available online under the Creative Commons Attribution-Share Alike license
(http://creativecommons.org/licenses/by-sa/3.0/). You can read the book at http://jythonbook.com or
check out the source at the book project on bitbucket at http://bitbucket.org/javajuneau/jythonbook/.

Foreword (Apress first edition)
===============================

I started using Python in 2003, and I fell in love with the language for a variety of reasons. The elegance
of Python’s whitespace based syntax, the well conceived built in data types, and a beautiful set of library
functions. Since that time, many other people have discovered or rediscovered Python. At the time of
this writing, the software industry is well into a resurgence of dynamically typed languages: Ruby, PHP,
and Python.
It wasn’t until I attended my first PyCon in 2004 that I became aware of Jython. People were glad of
the ability to run Python programs on the Java Virtual Machine (JVM), but were wistful because at the
time Jython was lagging behind the native C Python (CPython) interpreter in terms of supporting recent
versions of the language. Jython was maintained by a series of individual developers, but the task of
staying current with CPython was really too much for any single person. In December 2005, Frank
Wierzbicki took over as the lead developer for Jython, and over the next few years managed to foster a
community of developers for Jython. The authors of this book are some of the members of that
community. In June of 2009, the Jython community released Jython 2.5, which implemented the same
language as CPython 2.5. This was a major leap forward, bringing Jython much closer to feature parity
with CPython, and laying a foundation for catching up the rest of the way with CPython. Jython 2.5 is
able to run many of the most popular Python packages, including Django, Pylons, and SQLAlchemy.
Jython makes for a best of both worlds bridge between the elegant, expressive code of the Python
world and the “enterprise ready” Java world. Developers who work in organizations where Java is
already in use can now take advantage of the expressiveness and conciseness of Python by running their
Python programs on Jython. Jython provides easy integration and interoperability between Python code
and existing Java code.
Jython also has something to offer existing Python programmers, namely access to the very rich
ecosystem of the Java Virtual Machine. There is an enormous amount of Java code out in the world.
There are libraries for every task imaginable, and more. Jython gives Python programmers a way to tap
into these libraries, saving both development and testing time. Web applications running on Jython can
also take advantage of the scalability benefits of Java web containers such as Tomcat or GlassFish.
Things are looking very bright for Jython, and this book is a timely resource for people interested in
taking advantage of the benefits that Jython has to offer.


Ted Leung


Front Matter
============

.. toctree::
   :maxdepth: 2

   aboutTheAuthors.rst
   attribution.rst
   aboutTechReviewers.rst


Part I:  Jython Basics:  Learning the Language
==============================================

.. toctree::
   :maxdepth: 2

   LangSyntax.rst
   DataTypes.rst
   OpsExpressPF.rst
   DefiningFunctionsandUsingBuilt-Ins.rst
   InputOutput.rst
   ObjectOrientedJython.rst
   ExceptionHandlingDebug.rst
   ModulesPackages.rst


Part II: Using the Language
===========================

.. toctree::
   :maxdepth: 2

   Scripting.rst
   JythonAndJavaIntegration.rst
   JythonIDE.rst
   DatabasesAndJython.rst


Part III: Developing Applications with Jython
=============================================

.. toctree::
   :maxdepth: 2

   SimpleWebApps.rst
   JythonDjango.rst
   IntroToPylons.rst
   GUIApplications.rst
   DeploymentTargets.rst




Part IV:  Strategy and Technique
================================

.. toctree::
   :maxdepth: 2

   TestingIntegration.rst
   Concurrency.rst

Part V:  Appendices
===================

.. toctree::
   :maxdepth: 2

   appendixA.rst
   appendixB.rst
   appendixC.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



