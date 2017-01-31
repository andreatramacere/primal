""" Small example for a python based script """

import argparse
import ElementsKernel.Logging as log



def defineSpecificProgramOptions():
    """
    @brief Allows to define the (command line and configuration file) options specific to
    this program

    @details
        See the ElementsProgram documentation for more details.
    @return
        An  ArgumentParser.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--int-option', type=int,
                        help='An int example option')

    return parser

def mainMethod(args):
    """
    @brief The "main" method.
    @details This method is the entry point to the program. In this sense, it is similar to a main
    (and it is why it is called mainMethod()). The code below contains the calls to the
    different classes created for the first developer's workshop

        See the ElementsProgram documentation for more details.
    """
    logger = log.getLogger('SomeOtherScript')
    logger.info('Entering SomeOtherScript mainMethod()')

    #
    #  Log some of the arguments
    #
    int_from_configuration = args.int_option
    if not int_from_configuration:
        int_from_configuration = 9
    logger.info('Example int : %d', int_from_configuration)

    ThatFunction()

    logger.info('Exiting SomeOtherScript mainMethod()')

    return 0
