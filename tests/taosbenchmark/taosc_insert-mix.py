###################################################################
#           Copyright (c) 2016 by TAOS Technologies, Inc.
#                     All rights reserved.
#
#  This file is proprietary and confidential to TAOS Technologies.
#  No part of this file may be reproduced, stored, transmitted,
#  disclosed or used in any form or by any means other than as
#  expressly provided by the written permission from Jianhui Tao
#
###################################################################

# -*- coding: utf-8 -*-
import os
import subprocess

from util.log import *
from util.cases import *
from util.sql import *
from util.dnodes import *


class TDTestCase:
    def caseDescription(self):
        """
        taosBenchmark insert mix data
        """

    @classmethod
    def init(self, conn, logSql):
        tdLog.debug("start to execute %s" % __file__)
        tdSql.init(conn.cursor(), logSql)

    @classmethod
    def getPath(self, tool="taosBenchmark"):
        selfPath = os.path.dirname(os.path.realpath(__file__))

        if "community" in selfPath:
            projPath = selfPath[: selfPath.find("community")]
        elif "src" in selfPath:
            projPath = selfPath[: selfPath.find("src")]
        elif "/tools/" in selfPath:
            projPath = selfPath[: selfPath.find("/tools/")]
        elif "/tests/" in selfPath:
            projPath = selfPath[: selfPath.find("/tests/")]
        else:
            tdLog.info("cannot found %s in path: %s, use system's" % (tool, selfPath))
            projPath = "/usr/local/taos/bin/"

        paths = []
        for root, dummy, files in os.walk(projPath):
            if (tool) in files:
                rootRealPath = os.path.dirname(os.path.realpath(root))
                if "packaging" not in rootRealPath:
                    paths.append(os.path.join(root, tool))
                    break
        if len(paths) == 0:
            return ""
        return paths[0]

    @classmethod
    def run(self):
        binPath = self.getPath()
        # mix 1 ~ 4
        for i in range(4):
            cmd = "%s -f ./taosbenchmark/json/case-insert-mix%d.json"% (binPath, i+1)
            tdLog.info("%s" % cmd)
            os.system("%s" % cmd)

        psCmd = "ps -ef|grep -w taosBenchmark| grep -v grep | awk '{print $2}'"
        processID = subprocess.check_output(psCmd, shell=True)

        while processID:
            time.sleep(1)
            processID = subprocess.check_output(psCmd, shell=True)

        tdSql.query("select count(*) from mix1.meters")

    @classmethod
    def stop(self):
        tdSql.close()
        tdLog.success("%s successfully executed" % __file__)


tdCases.addWindows(__file__, TDTestCase())
tdCases.addLinux(__file__, TDTestCase())
