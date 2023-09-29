{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMEiPcsBxWVb5HVP20n5dQM",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/susiemoores/NRW_stats/blob/main/NRW_monthly_stats.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 15,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "UR8YVeiLUx_c",
        "outputId": "f583a9ff-6b2e-4851-e32e-df720c2d12bb"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Significant risk\n",
            "Elevated risk\n"
          ]
        }
      ],
      "source": [
        "# setting up\n",
        "import requests\n",
        "response = requests.get('https://api.ffc-environment-agency.fgs.metoffice.gov.uk/api/public/v1/statements/latest_public_forecast')\n",
        "response_content = response.content.decode('utf-8')\n",
        "import json\n",
        "data = json.loads(response_content)\n",
        "\n",
        "# risk areas\n",
        "risk_areas = data['statement']['risk_areas']\n",
        "days = [block['days'] for area in risk_areas for block in area['risk_area_blocks']]\n",
        "risk_levels =  [block['risk_levels'] for area in risk_areas for block in area['risk_area_blocks']]\n",
        "\n",
        "# days and risk\n",
        "dict_days = {idx+1: sublist for idx, sublist in enumerate(days)}\n",
        "dict_risk = {idx+1: sublist for idx, sublist in enumerate(risk_levels)}\n",
        "\n",
        "# counties\n",
        "polys = [block['polys'] for area in risk_areas for block in area['risk_area_blocks']]\n",
        "counties = {}\n",
        "for i, poly in enumerate(polys):\n",
        "     county_names = [county['name'] for county in poly[0]['counties']]\n",
        "     counties[i+1] = county_names\n",
        "\n",
        "wales_counties =  ['Blaenau Gwent', 'Bridgend', 'Caerphilly', 'Cardiff', 'Carmarthenshire', 'Ceredigion', 'Conwy', 'Denbighshire', 'Flintshire', 'Gwynedd', 'Isle of Anglesey', 'Merthyr Tydfil', 'Monmouthshire', 'Neath Port Talbot', 'Newport', 'Pembrokeshire', 'Powys', 'Rhondda Cynon Taff', 'Swansea', 'Torfaen', 'Vale of Glamorgan', 'Wrexham']\n",
        "\n",
        "# threshold risks\n",
        "minor = [key for key, value in dict_risk.items() if any(num[0] >= 2 for num in value.values())]\n",
        "significant = [key for key, value in dict_risk.items() if any(num[0] >= 3 for num in value.values())]\n",
        "\n",
        "# risk levels\n",
        "found_risk = False\n",
        "for key, value in dict_days.items():\n",
        "    if key in significant and 1 in value and key in counties and any(county in wales_counties for county in counties[key]):\n",
        "        print(\"Significant risk\")\n",
        "\n",
        "found_risk = False\n",
        "for key, value in dict_days.items():\n",
        "    if key in minor and 1 in value and key in counties and any(county in wales_counties for county in counties[key]):\n",
        "        print(\"Elevated risk\")\n",
        "        found_risk = True\n",
        "        break\n",
        "\n",
        "if not found_risk:\n",
        "    print(\"No elevated risk\")\n",
        "\n"
      ]
    }
  ]
}
